from rest_framework import serializers

from .models import Worksite


class WorksiteOutputSerializer(serializers.Serializer):
    worksite_id = serializers.IntegerField()
    sector = serializers.ChoiceField(choices=Worksite.sector_options)
    name = serializers.CharField()
    adress = serializers.CharField()
    postal_code = serializers.IntegerField()
    city = serializers.CharField()
    started = serializers.DateField()
    finished = serializers.DateField()
    status = serializers.ChoiceField(choices=Worksite.status_options)


class WorksiteInputSerializer(serializers.Serializer):
    sector = serializers.ChoiceField(choices=Worksite.sector_options)
    name = serializers.CharField()
    adress = serializers.CharField()
    postal_code = serializers.IntegerField()
    city = serializers.CharField()
    started = serializers.DateField()
    finished = serializers.DateField()
    status = serializers.ChoiceField(choices=Worksite.status_options)
