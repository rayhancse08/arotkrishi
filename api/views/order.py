from rest_framework import serializers
from api.models import OrderItem, Order, Merchant
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from django.core.exceptions import ValidationError
from api.views.product import ProductSerializer
from api.views.utils import MultipartJsonParser
from rest_framework.parsers import JSONParser
# from rest_framework import generics
# from rest_framework.utils import model_meta
from rest_framework.response import Response


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = (
            'id',
            'name',
        )


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'unit',
            'price',
        )


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'quantity',
            'unit',
            'price',
            'amount',
        )


class BlankableDecimalField(serializers.DecimalField):
    """
    We wanted to be able to receive an empty string ('') for a decimal field
    and in that case turn it into a None number
    """

    def to_internal_value(self, data):
        if data == '':
            return None

        return super(BlankableDecimalField, self).to_internal_value(data)


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True, required=False)
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    total_order = serializers.SerializerMethodField()

    # @staticmethod
    def get_total_order(self, obj):
        return self.context.get("user").merchant_user_permissions.first().merchant.orders.count()

    @staticmethod
    def create_update_order_items(order_items_data, order):
        # delete extras that are not added in the payload
        # items_ids = [order_item.get('id') for order_item in order_items_data if order_item.get('id', None)]
        # ProductExtra.objects.filter(product=product).exclude(id__in=extra_ids).update(
        #     is_active=False
        # )

        # create or update extras added in the payload
        for order_item in order_items_data:
            OrderItem.objects.update_or_create(
                order=order,
                id=order_item.get('id', None),
                defaults=order_item

            )

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order(**validated_data)
        merchant = self.context.get("user").merchant_user_permissions.first().merchant
        order.buyer = merchant
        try:
            order.clean()
            order.save()
        except ValidationError as e:
            raise serializers.ValidationError({"error": [e.message]})
        self.create_update_order_items(order_items_data, order)
        return order

    class Meta:
        model = Order

        fields = (
            'id',
            'order_date',
            'delivery_date',
            'status',
            # 'buyer',
            'created_by',
            'order_items',
            'total_order'

        )


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    buyer = MerchantSerializer(many=False)

    class Meta:
        model = Order
        fields = (
            'id',
            'order_date',
            'delivery_date',
            'buyer',
            'total_amount',
            'status',
            'created_by',
            'order_items',
            'created'

        )


class OrderViewSet(
    MultiSerializerMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = OrderSerializer

    parser_classes = (JSONParser, MultipartJsonParser)

    def get_queryset(self):
        merchant = self.request.user.merchant_user_permissions.first().merchant
        qs = Order.objects.filter(buyer=merchant)
        return qs

        # return Order.objects.all()

    def get_serializer_context(self):
        context = super(OrderViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    serializer_action_classes = {
        'list': OrderSerializer,
        'retrieve': OrderSerializer,
        'create': OrderCreateUpdateSerializer,
        'update': OrderCreateUpdateSerializer,
    }
