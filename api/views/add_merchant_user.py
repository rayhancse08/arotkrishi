from rest_framework import serializers
from api.models import MerchantPermission, UserProfile, Merchant
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import uuid
from api.views.profile import UserSerializer

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import generics
# import phonenumbers
# from phonenumbers.phonenumberutil import region_code_for_country_code

class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    # code = serializers.SerializerMethodField()
    # national_number = serializers.SerializerMethodField()
    # country_code = serializers.SerializerMethodField()

    @staticmethod
    def get_name(obj):
        return obj.profile.name

    @staticmethod
    def get_phone_number(obj):
        return obj.profile.phone_number

    # @staticmethod
    # def get_code(obj):
    #     pn = phonenumbers.parse(obj.profile.phone_number)
    #     return region_code_for_country_code(pn.country_code)
    #
    # @staticmethod
    # def get_national_number(obj):
    #     pn = phonenumbers.parse(obj.profile.phone_number)
    #     return pn.national_number
    #
    # @staticmethod
    # def get_country_code(obj):
    #     pn = phonenumbers.parse(obj.profile.phone_number)
    #     return "+{}".format(pn.country_code)

    class Meta:
        model = User
        fields = ('id',
                  'name',
                  'phone_number',
                  'email',
                  'address',
                  'profile_picture')
        # 'code',
        # 'country_code',
        # 'national_number')


class MerchantPermissionCreateUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=50, required=False)
    name = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=50, required=False)
    confirm_password = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number', None)
        name = validated_data.get('name', None)
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)
        # user = validated_data.get('user', None)
        create_permission = validated_data.get('create_permission', None)
        update_permission = validated_data.get('update_permission', None)
        delete_permission = validated_data.get('delete_permission', None)
        read_permission = validated_data.get('read_permission', None)
        # store = Store.objects.get(id=int(self.context.get("store_id")))
        merchant = self.context.get("user").merchant_user_permissions.first().merchant
        # user = self.context.get("user")
        # if not user:
        if not name:
                raise serializers.ValidationError({"error": "Name required"})

        if not phone_number:
                raise serializers.ValidationError({"error": "Phone number required"})

        if not password:
                raise serializers.ValidationError({"error": "Password required"})

        if password != confirm_password:
                raise serializers.ValidationError({"error": "Password not match"})
        user_profile = UserProfile.objects.filter(phone_number=phone_number).exists()
        if user_profile:
                raise serializers.ValidationError({"error": "User already exists"})
        user = User.objects.create_user(
                username=str(uuid.uuid4()),
                password=password
            )
        profile = UserProfile(user=user)
        profile.name = name
        profile.phone_number = phone_number
        profile.save()
        if MerchantPermission.objects.filter(user=user, merchant=merchant).exists():
            raise serializers.ValidationError({"error": "User already exists on this store"})

        merchant_permission = MerchantPermission(user=user, create_permission=create_permission,
                                                 update_permission=update_permission,
                                                 delete_permission=delete_permission, read_permission=read_permission,
                                                 merchant=merchant)
        merchant_permission.save()
        return merchant_permission

    class Meta:
        model = MerchantPermission
        extra_kwargs = {
            'phone_number': {'required': False},
            'password': {'required': False},
            'confirm_password': {'required': False},
            'user': {'required': False},
        }
        fields = (
            # 'user',
            'phone_number',
            'name',
            'password',
            'confirm_password',
            'create_permission',
            'update_permission',
            'delete_permission',
            'read_permission',
        )


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = (
            'id',
            'name',
        )


class MerchantPermissionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    merchant = MerchantSerializer()

    class Meta:
        model = MerchantPermission
        fields = (
            'id',
            'user',
            'merchant',
            'create_permission',
            'update_permission',
            'delete_permission',
            'read_permission',
            'owner',

        )


class MerchantUserPermissionViewSet(
    MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = MerchantPermissionSerializer

    def get_queryset(self):
        # user = self.request.user
        # store = self.request.META.get('HTTP_STORE_ID', None)
        merchant = self.request.user.merchant_user_permissions.first().merchant
        qs = MerchantPermission.objects.filter(merchant=merchant)
        return qs

    def get_serializer_context(self):
        context = super(MerchantUserPermissionViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    serializer_action_classes = {
        'list': MerchantPermissionSerializer,
        'retrieve': MerchantPermissionSerializer,
        'create': MerchantPermissionCreateUpdateSerializer,
        'update': MerchantPermissionCreateUpdateSerializer
    }
