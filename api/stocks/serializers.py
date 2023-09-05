from rest_framework import serializers

from ..products.models import Product
from ..products.serializers import ProductOutputSerializer
from ..worksites.models import Worksite
from ..worksites.serializers import WorksiteOutputSerializer


class StockInputSerializer(serializers.Serializer):
    worksite = serializers.PrimaryKeyRelatedField(queryset=Worksite.objects.all(), required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    quantity = serializers.IntegerField()


class StockOutputSerializer(serializers.Serializer):
    stock_id = serializers.IntegerField()
    worksite = WorksiteOutputSerializer()
    product = ProductOutputSerializer()
    quantity = serializers.IntegerField()
