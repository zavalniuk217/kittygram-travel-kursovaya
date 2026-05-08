from django.shortcuts import render
from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from cats.views import AchievementViewSet, CatViewSet, UserViewSet, TravelRouteViewSet, index

router = routers.DefaultRouter()
router.register('cats', CatViewSet)
router.register('users', UserViewSet)
router.register('achievements', AchievementViewSet)
router_travel = routers.DefaultRouter()
router_travel.register('travel/routes', TravelRouteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_travel.urls)),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
    path('home/', index, name='index'),  # 👈 ДОБАВЬТЕ ЭТУ СТРОКУ
]