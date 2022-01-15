
# Django REST framework
from rest_framework import status, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

# Models
from participants.models import Participant

# Serializer
from participants.serializers.list_participants import ListParticipantSerializer

class ParticipantViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """ List participants """

    queryset = Participant.objects.filter(type_of_participant='student')
    serializer_class = ListParticipantSerializer