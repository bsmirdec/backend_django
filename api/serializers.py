from rest_framework import serializers
from .models import Worksite, Client


class WorksiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksite
        fields = ("worksite_id", "name", "sector", "client", "city", "adress", "started", "status")


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]
