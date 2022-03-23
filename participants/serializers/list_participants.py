""" List all the participants """

# Django REST framework
from rest_framework import serializers

# Models
from participants.models import Participant, School

class SchoolModelSerializer(serializers.ModelSerializer):
    """ School model serializer """

    class Meta:
        model = School
        fields = ['name']

class ListParticipantSerializer(serializers.ModelSerializer):
    """ Participant model serializer """

    school = SchoolModelSerializer(read_only=True)
    class Meta:
        model = Participant
        fields = ['first_name',
                  'last_name',
                  'temp_user_name_omegaup',
                  'category',
                  'school',
                  'is_verified']