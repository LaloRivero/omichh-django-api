
# Django REST framework
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

# Models
from participants.models import Participant

# Serializer
from participants.serializers.list_participants import ListParticipantSerializer
from participants.serializers.create_participant import CreateParticipantSerializer

class ParticipantViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    ''' Participant model ViewSet '''

    queryset = Participant.objects.all()
    serializer_class = CreateParticipantSerializer

    def perform_create(self, serializer):
        ''' Create a new participant method '''
        serializer.save()


    def list(self, request, *args, **kwargs):
        ''' List all participants data '''
        queryset = Participant.objects.filter(type_of_participant='student')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ListParticipantSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ListParticipantSerializer(queryset, many=True)
        return Response(serializer.data)