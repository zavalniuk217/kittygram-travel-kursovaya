from django.contrib import admin
from .models import Cat, TravelRoute, TravelPoint, TravelBooking

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'birth_year')
    search_fields = ('name',)

@admin.register(TravelRoute)
class TravelRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'start_city', 'end_city', 'start_date', 'end_date', 'author')
    list_filter = ('start_city', 'end_city', 'start_date')
    search_fields = ('title', 'start_city', 'end_city')

@admin.register(TravelPoint)
class TravelPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'city', 'arrival_date', 'departure_date', 'order')

@admin.register(TravelBooking)
class TravelBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'participant', 'status', 'created_at')