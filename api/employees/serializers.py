from rest_framework import serializers

from ..serializers import ChoiceDisplayField
from .models import Employee


class PermissionsSerializer(serializers.JSONField):
    def to_representation(self, value):
        # Convertir le JSON en dictionnaire Python
        permissions_dict = super().to_representation(value)
        return permissions_dict

    def to_internal_value(self, data):
        # Convertir le dictionnaire Python en JSON
        return super().to_internal_value(data)


class EmployeeInputSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = ChoiceDisplayField(choices=Employee.positions_options)
    is_current = serializers.BooleanField()
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    permissions = PermissionsSerializer()
    threshold = serializers.IntegerField()


class EmployeeOutputSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = ChoiceDisplayField(choices=Employee.positions_options)
    is_current = serializers.BooleanField()
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    permissions = PermissionsSerializer()
    threshold = serializers.IntegerField()
