''' School model serializer '''

#Django REST framework
from rest_framework import serializers

#Models
from participants.models import School


class SchoolModelSerializer(serializers.ModelSerializer):
    ''' School model serializer '''

    class Meta:
        model=School
        fields = ['id','name', 'direction', 'principal_name', 'principal_email']