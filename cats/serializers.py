from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import TravelRoute, TravelPoint, TravelBooking

import datetime as dt

from .models import CHOICES, Achievement, AchievementCat, Cat, User


class UserSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'cats')
        ref_name = 'ReadOnlyUsers'


class AchievementSerializer(serializers.ModelSerializer):
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    color = serializers.ChoiceField(choices=CHOICES)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'achievements', 'owner',
                  'age')

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        if 'achievements' not in self.initial_data:
            cat = Cat.objects.create(**validated_data)
            return cat
        else:
            achievements = validated_data.pop('achievements')
            cat = Cat.objects.create(**validated_data)
            for achievement in achievements:
                current_achievement, status = Achievement.objects.get_or_create(
                    **achievement)
                AchievementCat.objects.create(
                    achievement=current_achievement, cat=cat)
            return cat

class TravelPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPoint
        fields = ('id', 'city', 'arrival_date', 'departure_date', 'order')


class TravelBookingSerializer(serializers.ModelSerializer):
    participant_username = serializers.ReadOnlyField(source='participant.username')
    
    class Meta:
        model = TravelBooking
        fields = ('id', 'participant', 'participant_username', 'status', 'created_at')
        read_only_fields = ('participant', 'created_at')


class TravelRouteSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    cats_names = serializers.StringRelatedField(source='cats', many=True, read_only=True)
    points = TravelPointSerializer(many=True, read_only=True)
    bookings_count = serializers.IntegerField(source='bookings.count', read_only=True)
    
    class Meta:
        model = TravelRoute
        fields = ('id', 'title', 'author', 'author_username', 'cats', 'cats_names',
                  'start_date', 'end_date', 'start_city', 'end_city', 
                  'description', 'points', 'bookings_count', 'created_at')
        read_only_fields = ('author', 'created_at')
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'end_date': 'Дата окончания не может быть раньше даты начала'
            })
        return data