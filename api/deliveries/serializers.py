from rest_framework import serializers

from .models import Delivery
from ..requests.models import Order, Retour
from ..worksites.models import Worksite
from ..products.models import Product
from ..requests.serializers import OrderOutputSerializer, RetourOutputSerializer
from ..products.serializers import ProductOutputSerializer
from ..worksites.serializers import WorksiteOutputSerializer


class StatusField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.status_mapping = {display: value for value, display in Delivery.status_options}
        super(StatusField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data in self.status_mapping:
            return self.status_mapping[data]
        return data

    def to_representation(self, value):
        for display, code in self.status_mapping.items():
            if code == value:
                return display
        return value


class DeliveryInputSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)
    worksite = serializers.PrimaryKeyRelatedField(queryset=Worksite.objects.all(), required=True)
    expected_date_time = serializers.DateTimeField()
    real_date_time = serializers.DateTimeField(required=False)
    status = StatusField(choices=Delivery.status_options, required=False)


class DeliveryOutputSerializer(serializers.Serializer):
    delivery_id = serializers.IntegerField()
    order = OrderOutputSerializer(required=False)
    worksite = WorksiteOutputSerializer()
    expected_date_time = serializers.DateTimeField()
    real_date_time = serializers.DateTimeField(required=False)
    status = StatusField(choices=Delivery.status_options, required=False)


class DeliveryLineInputSerializer(serializers.Serializer):
    delivery = serializers.PrimaryKeyRelatedField(queryset=Delivery.objects.all(), required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField()


class DeliveryLineOutputSerializer(serializers.Serializer):
    delivery_line_id = serializers.IntegerField()
    delivery = serializers.PrimaryKeyRelatedField(queryset=Delivery.objects.all(), required=True)
    product = ProductOutputSerializer()
    quantity = serializers.IntegerField()
