from rest_framework import serializers
from api.models import Merchant
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.views.utils import MultiSerializerMixin
from rest_framework.utils import model_meta
from api.views.utils import MultipartJsonParser
from rest_framework.parsers import MultiPartParser, FormParser


class BuyerSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):

        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.clean()
        instance.save()
        return instance

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
        extra_kwargs = {
            'logo': {'required': False},
            'nid': {'required': False},
            'trade_licence': {'required': False},
            'tin_certificate': {'required': False},
            'agreement': {'required': False},
            'phone_number': {'required': False},
            'address': {'required': False}
        }


class BuyerViewSet(MultiSerializerMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,

                   ):
    serializer_class = BuyerSerializer

    # parser_classes = (MultiPartParser, FormParser)

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
