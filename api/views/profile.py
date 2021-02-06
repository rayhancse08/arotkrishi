from rest_framework import viewsets, status
from rest_framework import serializers
from api import models
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import generics


class UserProfileSerializer(serializers.ModelSerializer):
    # @staticmethod
    # def get_id(obj):
    #     return obj.user.id

    class Meta:
        model = models.UserProfile
        fields = (
            'id',
            'name',
            'address',
            'email',
            'profile_picture',
            'phone_number',
            'initial_balance',
        )


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    @staticmethod
    def get_name(obj):
        return obj.profile.name

    @staticmethod
    def get_address(obj):
        return obj.profile.address

    @staticmethod
    def get_email(obj):
        return obj.profile.email

    @staticmethod
    def get_profile_picture(obj):
        if obj.profile.profile_picture:
            return obj.profile.profile_picture.url
        return ''

    @staticmethod
    def get_phone_number(obj):
        return obj.profile.phone_number

    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'address',
                  'email',
                  'profile_picture',
                  'phone_number',
                  )