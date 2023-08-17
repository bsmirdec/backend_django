from rest_framework import serializers

from .models import Worksite


class WorksiteOutputSerializer(serializers.Serializer):
    worksite_id = serializers.IntegerField()
    sector = serializers.ChoiceField(choices=Worksite.sector_options)
    client = serializers.CharField()
    name = serializers.CharField()
    address = serializers.CharField()
    postal_code = serializers.IntegerField()
    city = serializers.CharField()
    started = serializers.DateField()
    finished = serializers.DateField(required=False)
    status = serializers.ChoiceField(choices=Worksite.status_options)


class WorksiteInputSerializer(serializers.Serializer):
    sector = serializers.ChoiceField(choices=Worksite.sector_options)
    client = serializers.CharField()
    name = serializers.CharField()
    address = serializers.CharField()
    postal_code = serializers.IntegerField()
    city = serializers.CharField()
    started = serializers.DateField()
    finished = serializers.DateField(required=False)
    status = serializers.ChoiceField(choices=Worksite.status_options)
