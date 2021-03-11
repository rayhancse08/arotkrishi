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


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = (
            'id',
            'name',

            'phone_number',
            'email',
            'address',

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


class PaymentUpdateSerializer(serializers.ModelSerializer):
    # paid_by = UserListSerializer(many=False, read_only=True)
    # received_by = UserListSerializer(many=False, read_only=True)
    payment_id = serializers.IntegerField(required=False)

    class Meta:
        model = Payment
        fields = (
            'id',
            'payment_id',
            'bank_name',
            'branch_name',
            'check_no',
            'check_date',
            'payment_type',
            'partial_amount',
            'attachment',
            # 'received_by',
            # 'received',
            # 'paid_by',
            # 'created',
        )


class BillingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='order.id')
    order = OrderSerializer(many=False, read_only=True)
    payments = PaymentSerializer(many=True)
    buyer = serializers.SerializerMethodField()

    @staticmethod
    def get_buyer(obj):
        return BuyerSerializer(obj.order.buyer).data

    class Meta:
        model = Billing
        fields = (
            'id',
            'order',
            'amount',
            'status',
            'buyer',
            'payments'
        )


class BillingUpdateSerializer(serializers.ModelSerializer):
    # order = OrderSerializer(many=False)
    id = serializers.IntegerField(source='order.id', read_only=True)
    payments = PaymentUpdateSerializer(many=True, required=False)

    @staticmethod
    def create_update_payments(payments_data, billing, user):
        payment_id_list = []
        for payment in payments_data:
            # print(payment)
            payment_id = payment.get('payment_id', None)
            bank_name = payment.get('bank_name', None)
            branch_name = payment.get('branch_name', None)
            check_no = payment.get('check_no', None)
            check_date = payment.get('check_date', None)
            payment_type = payment.get('payment_type', None)
            partial_amount = payment.get('partial_amount', None)
            attachment = payment.get('attachment', None)
            # print(payment_id)
            if payment_id:
                payment_instance = Payment.objects.get(id=payment_id)
                payment_instance.bank_name = bank_name
                payment_instance.branch_name = branch_name
                payment_instance.check_no = check_no
                payment_instance.check_date = check_date
                payment_instance.payment_type = payment_type
                payment_instance.partial_amount = partial_amount
                if attachment:
                    payment_instance.attachment = attachment
                payment_instance.clean()
                payment_instance.save()
                payment_id_list.append(payment_instance.id)
            else:
                payment_instance = Payment(billing=billing, bank_name=bank_name, branch_name=branch_name,
                                           check_no=check_no, check_date=check_date,
                                           payment_type=payment_type, partial_amount=partial_amount,
                                           attachment=attachment, payment_date=localtime().date(), paid_by=user)
                try:
                    payment_instance.clean()
                    payment_instance.save()
                    payment_id_list.append(payment_instance.id)
                except ValidationError as e:
                    raise serializers.ValidationError({"error": [e.message]})
            billing.payments.exclude(id__in=payment_id_list).delete()

    def update(self, instance, validated_data):
        # bank_name = validated_data.get('bank_name', None)
        # if not instance.payment_date and bank_name:
        #     instance.payment_date = localtime().date()
        #     instance.paid_by = self.context.get("user")
        if 'payments' in validated_data:
            payments = validated_data.pop('payments')
            self.create_update_payments(payments, instance, user=self.context.get("user"))
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
            'payments',

        )


class BillingViewSet(MultiSerializerMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,

                     ):
    serializer_class = BillingSerializer
    lookup_field = 'order_id'
    parser_classes = (JSONParser, MultipartJsonParser)

    def get_queryset(self):
        merchant = self.request.user.merchant_user_permissions.first().merchant
        # store = self.request.META.get('HTTP_STORE_ID', None)
        qs = Billing.objects.filter(order__buyer=merchant)
        return qs

    def get_serializer_context(self):
        context = super(BillingViewSet, self).get_serializer_context()
        context['user'] = self.request.user
        return context

    serializer_action_classes = {
        'list': BillingSerializer,
        'retrieve': BillingSerializer,
        # 'create': OrderCreateUpdateSerializer,
        # 'update': BillingUpdateSerializer,
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
