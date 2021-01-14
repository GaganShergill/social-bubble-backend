from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = [
            'eventName',
            'eventType',
            'venue',
            'price',
            'details',
            'date',
            ]

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = [
            'activityName',
            'activityType',
            'venue',
            'price',
            'details',
            'date',
            ]

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = [
            'destination',
            'nights',
            'price',
            'details',
            'date',
            ]

class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'avatar',
        ]

    def validate(self, data):
        if not data['first_name'].isalpha():
            raise serializers.ValidationError({'first_name': "name must contain only alphabets"})
        if len(data['password']) < 8:
            raise serializers.ValidationError({'password': "password must be atleast 8 characters long"})
        return data

    def get_avatar(self, user):
        request = self.context.get('request')
        return request.build_absolute_uri(user.get_avatar_url())
