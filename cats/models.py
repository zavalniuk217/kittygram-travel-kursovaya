from django.contrib.auth import get_user_model
from django.db import models

CHOICES = (
    ('Gray', 'Серый'),
    ('Black', 'Чёрный'),
    ('White', 'Белый'),
    ('Ginger', 'Рыжий'),
    ('Mixed', 'Смешанный'),
)

User = get_user_model()


class Achievement(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES)
    birth_year = models.IntegerField()
    owner = models.ForeignKey(
        User, related_name='cats', on_delete=models.CASCADE)
    achievements = models.ManyToManyField(Achievement, through='AchievementCat')

    def __str__(self):
        return self.name


class AchievementCat(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.achievement} {self.cat}'


class TravelRoute(models.Model):
    """Модель маршрута путешествия"""
    title = models.CharField(max_length=100, verbose_name="Название маршрута")
    author = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        related_name='travel_routes',
        verbose_name="Автор"
    )
    cats = models.ManyToManyField('Cat', related_name='travel_routes', verbose_name="Котики")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    start_city = models.CharField(max_length=100, verbose_name="Город отправления")
    end_city = models.CharField(max_length=100, verbose_name="Город прибытия")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Маршрут путешествия"
        verbose_name_plural = "Маршруты путешествий"
        unique_together = ('author', 'title')
    
    def __str__(self):
        return self.title


class TravelPoint(models.Model):
    """Промежуточная точка маршрута"""
    route = models.ForeignKey(
        TravelRoute, 
        on_delete=models.CASCADE, 
        related_name='points',
        verbose_name="Маршрут"
    )
    city = models.CharField(max_length=100, verbose_name="Город")
    arrival_date = models.DateField(verbose_name="Дата прибытия")
    departure_date = models.DateField(verbose_name="Дата убытия")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок следования")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Точка маршрута"
        verbose_name_plural = "Точки маршрута"
    
    def __str__(self):
        return f"{self.route.title} - {self.city}"


class TravelBooking(models.Model):
    """Бронирование участия в путешествии"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('approved', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('completed', 'Завершено'),
    ]
    
    route = models.ForeignKey(
        TravelRoute, 
        on_delete=models.CASCADE, 
        related_name='bookings',
        verbose_name="Маршрут"
    )
    participant = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        related_name='travel_bookings',
        verbose_name="Участник"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('route', 'participant')
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
    
    def __str__(self):
        return f"{self.participant.username} -> {self.route.title}"


class WishlistItem(models.Model):
    """Потребность кота (Wishlist)"""
    cat = models.ForeignKey(
        Cat, 
        on_delete=models.CASCADE, 
        related_name='wishlist_items',
        verbose_name="Котик"
    )
    title = models.CharField(max_length=100, verbose_name="Название потребности")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_completed = models.BooleanField(default=False, verbose_name="Выполнено/куплено")
    travel_route = models.ForeignKey(
        TravelRoute, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='wishlist_items',
        verbose_name="Связанный маршрут"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Потребность кота (Wishlist)"
        verbose_name_plural = "Потребности котов (Wishlist)"

    def __str__(self):
        return f"{self.cat.name}: {self.title}"