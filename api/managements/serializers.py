from rest_framework import serializers


class ManagementSerializer(serializers.Serializer):
    worksite_id = serializers.IntegerField()
    employee_id = serializers.IntegerField()
