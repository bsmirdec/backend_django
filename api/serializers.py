from rest_framework import serializers
from .models import Client, Worksite, Administrator, SiteDirector, SiteSupervisor, SiteForeman, Management


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = "__all__"


class SiteDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteDirector
        fields = "__all__"


class SiteSupervisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSupervisor
        fields = "__all__"


class SiteForemanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteForeman
        fields = "__all__"


class WorksiteSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta:
        model = Worksite
        fields = "__all__"


class WorksiteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksite
        fields = "__all__"


class ManagementSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()

    def get_staff(self, obj):
        if isinstance(obj.staff, SiteDirector):
            return SiteDirectorSerializer(obj.staff).data
        elif isinstance(obj.staff, SiteSupervisor):
            return SiteSupervisorSerializer(obj.staff).data
        elif isinstance(obj.staff, SiteForeman):
            return SiteForemanSerializer(obj.staff).data

    class Meta:
        model = Management
        fields = ["staff", "worksite", "staff_type"]
