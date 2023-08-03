from rest_framework import serializers

from .models import Employee


class EmployeeInputSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = serializers.ChoiceField(choices=Employee.positions_options)
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    permissions = serializers.DictField()


class EmployeeOutputSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = serializers.ChoiceField(choices=Employee.positions_options)
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    permissions = serializers.DictField()
