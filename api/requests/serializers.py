from rest_framework import serializers

from .models import Order, Retour, Request
from ..worksites.models import Worksite
from ..products.models import Product
from ..products.serializers import ProductOutputSerializer
from ..worksites.serializers import WorksiteOutputSerializer


class StatusField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.status_mapping = {display: value for value, display in Request.status_options}
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


class RequestSerializer(serializers.Serializer):
    worksite = serializers.PrimaryKeyRelatedField(queryset=Worksite.objects.all(), required=True)
    date_time = serializers.DateTimeField()
    threshold = serializers.IntegerField()
    validation = serializers.IntegerField(required=False)
    status = StatusField(choices=Request.status_options, required=False)


class OrderOutputSerializer(RequestSerializer):
    worksite = WorksiteOutputSerializer()
    order_id = serializers.IntegerField()
    status = StatusField(choices=Request.status_options, required=False)


class RetourOutputSerializer(RequestSerializer):
    retour_id = serializers.IntegerField()


class RequestLineInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField()


class OrderLineInputSerializer(RequestLineInputSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)


class RetourLineInputSerializer(RequestLineInputSerializer):
    retour = serializers.PrimaryKeyRelatedField(queryset=Retour.objects.all(), required=True)


class RequestLineOutputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField()


class OrderLineOutputSerializer(RequestLineOutputSerializer):
    order_line_id = serializers.IntegerField()
    product = ProductOutputSerializer()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)


class RetourLineOutputSerializer(RequestLineOutputSerializer):
    retour = serializers.PrimaryKeyRelatedField(queryset=Retour.objects.all(), required=True)
