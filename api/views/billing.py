from rest_framework import serializers
from api.models import Billing, Order
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from rest_framework import generics
from rest_framework.utils import model_meta
from django.utils.timezone import localtime, now
from api.views.order import OrderSerializer

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ('id',
#                   'order_no')


class BillingSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False, read_only=True)

    class Meta:
        model = Billing
        fields = (
            'id',
            'order',
            'amount',
            'status',
            'received',
            'payment_date',
            'bank_name',
            'branch_name',
            'check_no',
            'check_date',
            'payment_type',
            'partial_amount',
            'attachment',
        )


class BillingUpdateSerializer(serializers.ModelSerializer):
    # order = OrderSerializer(many=False)
    def update(self, instance, validated_data):
        bank_name = validated_data.get('bank_name',None)
        if not instance.payment_date and bank_name:
            instance.payment_date = localtime().date()
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        instance.save()

        return instance

    class Meta:
        model = Billing
        fields = (
            'id',
            'bank_name',
            'branch_name',
            'check_no',
            'check_date',
            'payment_type',
            'partial_amount',
            'attachment',
        )


class BillingViewSet(MultiSerializerMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,

                     ):
    serializer_class = BillingSerializer

    def get_queryset(self):
        merchant = self.request.user.merchant_user_permissions.first().merchant
        # store = self.request.META.get('HTTP_STORE_ID', None)
        qs = Billing.objects.filter(order__buyer=merchant)
        return qs

    serializer_action_classes = {
        'list': BillingSerializer,
        'retrieve': BillingSerializer,
        # 'create': OrderCreateUpdateSerializer,
        'update': BillingUpdateSerializer,
    }


class BillingSearchView(generics.ListAPIView):
    serializer_class = BillingSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        merchant = self.request.user.merchant_user_permissions.first().merchant
        queryset = Billing.objects.filter(order__buyer=merchant)
        status = self.request.query_params.get('status', None)
        payment_from_date = self.request.query_params.get('payment_from_date', None)
        payment_to_date = self.request.query_params.get('payment_to_date', None)

        if status:
            queryset = queryset.filter(status__iexact=status)
        if payment_from_date and payment_to_date:
            queryset = queryset.filter(payment_date__gte=payment_from_date, payment_date__lte=payment_to_date)

        return queryset
