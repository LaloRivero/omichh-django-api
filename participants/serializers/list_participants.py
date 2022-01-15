""" List all the participants """

# Django REST framework
from rest_framework import serializers

# Models
from participants.models import Participant

class ListParticipantSerializer(serializers.ModelSerializer):
    """ Participant model serializer """

    class Meta:
        model = Participant
        fields = ['type_of_participant',
                  'first_name',
                  'last_name',
                  'temp_user_name_omegaup',
                  'category',
                  'school__name',
                  'is_verified']