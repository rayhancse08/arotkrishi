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
from rest_framework.utils import model_meta
from rest_framework.decorators import api_view


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
        order_item_id = []
        for order_item in order_items_data:
            product = order_item.get('product', None)
            quantity = order_item.get('quantity', None)
            price = order_item.get('price', None)
            unit = order_item.get('unit', None)
            if OrderItem.objects.filter(order=order, product=product).exists():
                order_item_instance = OrderItem.objects.filter(order=order, product=product).first()
                order_item_instance.unit = unit
                order_item_instance.quantity = quantity
                order_item_instance.price = price
                order_item_instance.save()
                order_item_id.append(order_item_instance.id)
            else:
                order_item_instance = OrderItem(order=order, product=product, quantity=quantity,
                                                price=price, unit=unit)
                try:
                    order_item_instance.clean()
                    order_item_instance.save()
                    order_item_id.append(order_item_instance.id)
                except ValidationError as e:
                    raise serializers.ValidationError({"error": [e.message]})
            order.order_items.exclude(id__in=order_item_id).delete()

            # OrderItem.objects.update_or_create(
            #     order=order,
            #     id=order_item.get('id', None),
            #     defaults=order_item
            #
            # )

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

    def update(self, instance, validated_data):
        if 'order_items' in validated_data:
            order_items_data = validated_data.pop('order_items')
            self.create_update_order_items(order_items_data, instance)
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        # if not purchase.user:
        #     purchase.user = user

        instance.clean()
        instance.save()

        return instance

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
    # status = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')

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


@api_view(['PUT'])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        # if not order.is_order_cancel_time_left():
        #     raise CancellationTimeExpired("You can not cancel order within 24 hours of delivery time")

        # if order.status_id in [CANCELLATION_PENDING, CANCELLED]:
        #     raise AlreadyCancelledException("Order is already cancelled")

        # if order.status_id not in [PENDING, PROCESSING, CONFIRMED, DELIVERY_CONFIRMED]:
        #     raise UnauthorizedException("You can not cancel this order")

        # status = OrderStatus.objects.get(id=CANCELLED)
        order.status = 3
        order.save()

        return Response(status=200, data={
            # "data": {
            #     "status": OrderStatusSerializer(order.status).data
            # },
            "message": "Order was successfully cancelled"
        })
    except Order.DoesNotExist:
        return Response(status=404, data={
            "error": {"message": "Order does not exist"}
        })
    # except AlreadyCancelledException as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except UnauthorizedException as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except CancellationTimeExpired as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except:
    #     return Response(status=403, data={
    #         "error": {"message": "Invalid request"}
    #     })


@api_view(['PUT'])
def confirm_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)

        # if not order.is_order_cancel_time_left():
        #     raise CancellationTimeExpired("You can not cancel order within 24 hours of delivery time")

        # if order.status_id in [CANCELLATION_PENDING, CANCELLED]:
        #     raise AlreadyCancelledException("Order is already cancelled")

        # if order.status_id not in [PENDING, PROCESSING, CONFIRMED, DELIVERY_CONFIRMED]:
        #     raise UnauthorizedException("You can not cancel this order")

        # status = OrderStatus.objects.get(id=CANCELLED)
        order.status = 4
        order.save()

        return Response(status=200, data={
            # "data": {
            #     "status": OrderStatusSerializer(order.status).data
            # },
            "message": "Order was successfully confirmed"
        })
    except Order.DoesNotExist:
        return Response(status=404, data={
            "error": {"message": "Order does not exist"}
        })
    # except AlreadyCancelledException as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except UnauthorizedException as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except CancellationTimeExpired as e:
    #     return Response(status=403, data={
    #         "error": {"message": str(e)}
    #     })
    # except:
    #     return Response(status=403, data={
    #         "error": {"message": "Invalid request"}
    #     })
