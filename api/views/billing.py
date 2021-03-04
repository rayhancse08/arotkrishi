from rest_framework import serializers
from api.models import Billing, Order
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin


# from api.views.order import OrderSerializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'order_no')


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
