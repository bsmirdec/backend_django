from rest_framework import serializers

from .models import Category, Type


class CategoryOutputSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField()


class TypeOutputSerializer(serializers.Serializer):
    type_id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    threshold = serializers.IntegerField()


class ProductOutputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    category = CategoryOutputSerializer()
    type = TypeOutputSerializer()
    name = serializers.CharField()
    brand = serializers.CharField()
    model = serializers.CharField()
    packaging = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    height = serializers.DecimalField(max_digits=10, decimal_places=2)
    length = serializers.DecimalField(max_digits=10, decimal_places=2)
    width = serializers.DecimalField(max_digits=10, decimal_places=2)
