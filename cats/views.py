from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Achievement, Cat, User, TravelRoute, TravelBooking, TravelPoint, WishlistItem
from .serializers import AchievementSerializer, CatSerializer, UserSerializer, TravelRouteSerializer, TravelBookingSerializer, TravelPointSerializer, WishlistItemSerializer
from .permissions import IsOwnerOrReadOnly

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class TravelRouteViewSet(viewsets.ModelViewSet):
    """ViewSet для маршрутов путешествий"""
    queryset = TravelRoute.objects.all()
    serializer_class = TravelRouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['start_city', 'end_city', 'start_date', 'end_date']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def join(self, request, pk=None):
        """Забронировать участие в путешествии"""
        route = self.get_object()
        
        # Проверка: нельзя присоединиться к своему маршруту
        if route.author == request.user:
            return Response(
                {'detail': 'Нельзя присоединиться к своему путешествию'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка: уже ли забронировал
        if TravelBooking.objects.filter(route=route, participant=request.user).exists():
            return Response(
                {'detail': 'Вы уже забронировали это путешествие'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Создаём бронирование
        booking = TravelBooking.objects.create(
            route=route,
            participant=request.user,
            status='pending'
        )
        
        serializer = TravelBookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def leave(self, request, pk=None):
        """Отменить бронирование"""
        route = self.get_object()
        
        try:
            booking = TravelBooking.objects.get(route=route, participant=request.user)
            booking.delete()
            return Response({'detail': 'Вы вышли из путешествия'}, status=status.HTTP_200_OK)
        except TravelBooking.DoesNotExist:
            return Response(
                {'detail': 'Вы не бронировали это путешествие'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def matches(self, request, pk=None):
        """Поиск маршрутов с пересекающимися городами"""
        route = self.get_object()
        route_cities = [route.start_city, route.end_city]
        
        matching_routes = TravelRoute.objects.exclude(id=route.id).filter(
            models.Q(start_city__in=route_cities) |
            models.Q(end_city__in=route_cities)
        ).distinct()
        
        serializer = TravelRouteSerializer(matching_routes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='points', permission_classes=[permissions.IsAuthenticated])
    def add_point(self, request, pk=None):
        """Добавить промежуточную точку маршрута"""
        route = self.get_object()
        
        # Проверка: только владелец или администратор может добавлять точки
        if request.user != route.author and not request.user.is_staff:
            return Response(
                {'detail': 'Только владелец маршрута может добавлять точки'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TravelPointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(route=route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistItemViewSet(viewsets.ModelViewSet):
    """ViewSet для управления Wishlist (потребностями котиков)"""
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(cat__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def toggle_completed(self, request, pk=None):
        """Переключить статус выполнения (выполнено/не выполнено)"""
        item = self.get_object()
        item.is_completed = not item.is_completed
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


def index(request):
    from django.shortcuts import render
    return render(request, 'cats/index.html')