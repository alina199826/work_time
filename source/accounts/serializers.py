
from rest_framework import  serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    # organization = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

    # def get_organization(self, user):
    #     try:
    #         organization = user.organization.name
    #     except AttributeError:
    #         organization = 'No organization'
    #     return organization