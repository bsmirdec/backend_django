from rest_framework import serializers


class NotificationInputSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    content = serializers.CharField()
    link = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    is_read = serializers.BooleanField()


class NotificationOutputSerializer(serializers.Serializer):
    notif_id = serializers.IntegerField()
    employee_id = serializers.IntegerField()
    content = serializers.CharField()
    link = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    is_read = serializers.BooleanField()
