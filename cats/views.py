from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from .models import Achievement, Cat, User, TravelRoute, TravelBooking
from .serializers import AchievementSerializer, CatSerializer, UserSerializer, TravelRouteSerializer, TravelBookingSerializer
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


def index(request):
    from django.shortcuts import render
    return render(request, 'cats/index.html')