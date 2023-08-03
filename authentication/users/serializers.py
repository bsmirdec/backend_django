from rest_framework import serializers


class UserInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserOutputSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login = serializers.DateTimeField()
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    is_validated = serializers.BooleanField()
