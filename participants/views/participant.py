
# Django REST framework
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Models
from participants.models import Participant

# Serializer
from participants.serializers.list_participants import ListParticipantSerializer
from participants.serializers.create_participant import CreateParticipantSerializer
from participants.serializers.account_verification import AccountVerificationSerializer

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


@api_view(['POST'])
def participant_verification(request):
    ''' Participant email verification '''

    if request.method == 'POST':
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {'message': 'Account verification success'}

        return Response(data, status=status.HTTP_200_OK)