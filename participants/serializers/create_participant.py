""" Create a new participant serializer """

# Django
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Models
from django.contrib.auth.models import User
from participants.models import Participant, School, Scores

# Utilities
import jwt
from datetime import timedelta

class CreateParticipantSerializer(serializers.Serializer):
    """ Handle the inscription of a participant and validate
    the user account by the email.
    """

    type_of_participant = serializers.CharField(max_length=50, allow_blank=False)
    first_name = serializers.CharField(max_length=100, allow_blank=False)
    last_name = serializers.CharField(max_length=100, allow_blank=False)
    email = serializers.EmailField(max_length=150, allow_blank=False)
    birthday = serializers.CharField(max_length=150, allow_blank=False)

    town = serializers.CharField(max_length=150, allow_blank=False)
    category = serializers.CharField(max_length=4, allow_blank=False)

    def create(self,data):
        """ Handle participant creation"""

        participant = Participant.objects.create(type_of_participant=data['type_of_participant'],
                                                first_name=data['first_name'],
                                                last_name=data['last_name'],
                                                email=data['email'],
                                                birthday=data['birthday'],
                                                town=data['town'],
                                                category=data['category'])

        participant.save()

        self.send_confirmation_email(participant)

        return participant


    def send_confirmation_email(self, participant):
        """ Send a confirmation email to verify the participant  """

        verification_token = self.gen_verification_token(participant)
        subject = f'Welcome @{user.username}! Verify your account to start using the App.'
        from_email = 'Application <noreply@app.com>'
        content = render_to_string(
            'emails/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """ Create a JWT token that the user can user to verify its account. """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token