''' Account verification serializer'''

#Django
from django.conf import settings

#Django REST framework
from rest_framework import serializers

#Model
from participants.models import Participant

#utilities
import jwt

class AccountVerificationSerializer(serializers.Serializer):
    ''' Account verification serializer'''

    token = serializers.CharField()

    def validate_token(self, data):
        ''' Verify if token is valid '''

        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({'Error':'Verification link has expired'})
        except jwt.PyJWKError:
            raise serializers.ValidationError({'Error': 'Invalid token'})

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError({'Error':'Invalid token'})

        self.context['payload'] = payload

        return data

    def save(self):
        ''' Update participan verified status '''

        payload = self.context['payload']
        participant = Participant.objects.get(email=payload["participant"])
        participant.is_verified = True
        participant.save()
        return participant