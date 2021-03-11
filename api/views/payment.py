from rest_framework import serializers
from api.models import Billing, Merchant, Payment
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from rest_framework import generics
from rest_framework.utils import model_meta
from django.utils.timezone import localtime, now
from api.views.order import OrderSerializer
from api.views.profile import UserListSerializer
from django.core.exceptions import ValidationError
from api.views.utils import MultipartJsonParser
from rest_framework.parsers import JSONParser


class PaymentCreateUpdateSerializer(serializers.ModelSerializer):
    # paid_by = UserListSerializer(many=False, read_only=True)
    # received_by = UserListSerializer(many=False, read_only=True)
    paid_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def create(self, validated_data):
        # store = Store.objects.get(id=int(self.context.get("store_id")))
        payment = Payment(**validated_data)
        payment.payment_date = localtime().date()
        payment.clean()
        payment.save()
        return payment

    class Meta:
        model = Payment
        fields = (
            'id',
            'billing',
            'bank_name',
            'branch_name',
            'check_no',
            'check_date',
            'payment_type',
            'partial_amount',
            'attachment',
            'paid_by',
        )


class PaymentSerializer(serializers.ModelSerializer):
    paid_by = UserListSerializer(many=False, read_only=True)
    received_by = UserListSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = (
            'id',
            'payment_date',
            'bank_name',
            'branch_name',
            'check_no',
            'check_date',
            'payment_type',
            'partial_amount',
            'attachment',
            'received_by',
            'received',
            'paid_by',
            'created',
        )


class PaymentViewSet(MultiSerializerMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,

                     ):
    serializer_class = PaymentSerializer

    # lookup_field = 'order_id'
    # parser_classes = (JSONParser, MultipartJsonParser)

    def get_queryset(self):
        # merchant = self.request.user.merchant_user_permissions.first().merchant
        # store = self.request.META.get('HTTP_STORE_ID', None)
        qs = Payment.objects.all()
        return qs

    def get_serializer_context(self):
        context = super(PaymentViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    serializer_action_classes = {
        'list': PaymentSerializer,
        'retrieve': PaymentSerializer,
        'create': PaymentCreateUpdateSerializer,
        'update': PaymentCreateUpdateSerializer,
    }
