from rest_framework import serializers

from webapp.models import WorkTime, Organization, Branch


class WorkTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTime
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_duration_hours(self, obj):
        duration = obj.end_time - obj.start_time
        return round(duration.total_seconds() / 3600, 2)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ['id']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ['id']
