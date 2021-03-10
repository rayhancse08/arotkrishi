from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from api.views.profile import UserProfileSerializer, UserSerializer
from api.models import UserProfile, Merchant, MerchantPermission
# from rest_framework import mixins
# from rest_framework.viewsets import GenericViewSet
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class UserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50)

    class Meta:
        model = UserProfile
        fields = ('phone_number', 'password')


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = (
            'id',
            'name'
        )


class MerchantPermissionSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer()

    class Meta:
        model = MerchantPermission
        fields = (
            'id',
            'merchant',
            'create_permission',
            'update_permission',
            'read_permission',
            'delete_permission',
            'owner',
            'user_type',

        )


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class LoginView(APIView):
    permission_classes = []
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = UserPasswordSerializer

    # @csrf_exempt
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            raise serializers.ValidationError({"error": "Phone number required"})
        password = request.data.get('password')
        if not password:
            raise serializers.ValidationError({"error": "Password required"})
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            username = UserProfile.objects.filter(phone_number=phone_number).first().user.username
            user = authenticate(username=username, password=password)
            if user:
                merchants = user.merchant_user_permissions.all()
                merchant_list = []
                for merchant in merchants:
                    merchant_list.append(MerchantPermissionSerializer(merchant).data)

                token, created = Token.objects.get_or_create(user=user)
                profile = UserSerializer(user, context={'request': request}).data
                return Response({
                    'token': token.key,
                    'user': profile,
                    'user_permission': merchant_list,

                }, )

            return Response({'error': 'Wrong Password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        if Token.objects.filter(user=request.user).exists():
            request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# class StoreViewSet(GenericViewSet,
#                    mixins.ListModelMixin,
#                    mixins.RetrieveModelMixin, ):
#     serializer_class = StorePermissionSerializer
#
#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = StorePermission.objects.filter(user=self.request.user)
#
#         return queryset
