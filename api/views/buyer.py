from rest_framework import serializers
from api.models import Merchant
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = (
            'id',
            'name',
            'logo',
            'phone_number',
            'email',
            'address',
            'nid',
            'trade_licence',
            'tin_certificate',
            'md_contact_details',
            'agreement'
        )


class BuyerViewSet(MultiSerializerMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,

                   ):
    serializer_class = BuyerSerializer

    def get_queryset(self):
        merchant = self.request.user.merchant_user_permissions.first().merchant.id
        # store = self.request.META.get('HTTP_STORE_ID', None)
        qs = Merchant.objects.filter(id=merchant, type=1)
        return qs

    serializer_action_classes = {
        'list': BuyerSerializer,
        'retrieve': BuyerSerializer,
        # 'create': OrderCreateUpdateSerializer,
        'update': BuyerSerializer,
    }
