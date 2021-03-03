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
    order = OrderSerializer(many=False,read_only=True)

    class Meta:
        model = Billing
        fields = (
            'id',
            'order',
            'amount',
            'status',
            'received',
        )


class BillingUpdateSerializer(serializers.ModelSerializer):
    # order = OrderSerializer(many=False)

    class Meta:
        model = Billing
        fields = (
            'id',
            # 'order',
            # 'amount',
            'status',
            # 'received',
        )


class BillingViewSet(mixins.UpdateModelMixin,
                     GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     MultiSerializerMixin,
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
