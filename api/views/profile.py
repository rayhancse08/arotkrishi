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
            # 'id',
            'name',
            'address',
            'email',
            'profile_picture',
            'phone_number',
            # 'initial_balance',
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


class ProfileViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """ Get currently logged in users profile. """
        return Response({
            'data': UserProfileSerializer(request.user.profile).data
        })

    def update(self, request, *args, **kwargs):
        """ Update currently logged in users profile. """
        partial = kwargs.pop('partial', False)
        name = request.data.get('name', None)
        phone_number = request.data.get('phone_number', None)

        if not name:
            raise serializers.ValidationError({'name': 'Name should not empty'})
        if not phone_number:
            raise serializers.ValidationError({'phone_number': 'Phone number should not empty'})

        profile_data = UserProfileSerializer(
            data=request.data,
            instance=request.user.profile,
            partial=partial
        )

        if profile_data.is_valid():
            profile_data.save(user=request.user)
            response = {'success': {
                'message': 'Profile updated successfully'
            }}

            if not partial:
                response['data'] = UserProfileSerializer(request.user.profile).data

            return Response(response, status=status.HTTP_200_OK)

        response = {'error': profile_data.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



