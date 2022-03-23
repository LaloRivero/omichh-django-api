""" Create a new participant serializer """

# Django
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField

# Models
from participants.models import Participant, School, Scores

# Serializers
from participants.serializers.school import SchoolModelSerializer

# Utilities
import jwt
from datetime import timedelta

class CreateParticipantSerializer(serializers.ModelSerializer):
    """ Handle the inscription of a participant and validate
    the user account by the email.
    """

    school = serializers.SlugRelatedField(queryset=School.objects.all(), slug_field='id')
    class Meta:
        model = Participant
        fields = ['type_of_participant',
                  'first_name',
                  'last_name',
                  'email',
                  'birthday',
                  'school',
                  'grade',
                  'phone',
                  'town',
                  'category',
                  'tutor_name',
                  'tutor_phone',
                  'tutor_email']


    def validate(self, data):
        ''' Validate the data from a new participant '''
        email = data['email']
        tutor_email = data['tutor_email']

        if email == tutor_email:
            raise serializers.ValidationError({'ERROR':'participant email and tutor email must to be different'})

        return data

    def create(self,validated_data):
        """ Handle participant creation"""
        print(validated_data)

        school = School.objects.get(id=validated_data["school"].id)

        participant = Participant(type_of_participant=validated_data['type_of_participant'],
                                                first_name=validated_data['first_name'],
                                                last_name=validated_data['last_name'],
                                                email=validated_data['email'],
                                                birthday=validated_data['birthday'],
                                                grade=validated_data['grade'],
                                                school=school,
                                                phone=validated_data['phone'],
                                                town=validated_data['town'],
                                                category=validated_data['category'],
                                                tutor_name=validated_data['tutor_name'],
                                                tutor_phone=validated_data['tutor_phone'],
                                                tutor_email=validated_data['tutor_email'])

        participant.save()

        self.send_confirmation_email(participant)

        return participant


    def send_confirmation_email(self, participant):
        """ Send a confirmation email to verify the participant  """

        verification_token = self.gen_verification_token(participant)
        subject = f'Welcome @{participant.first_name} {participant.last_name}! Verify your account to start using the App.'
        from_email = 'Application <noreply@app.com>'
        content = render_to_string(
            'emails/account_verification.html',
            {'token': verification_token, 'participant': participant}
        )
        msg = EmailMultiAlternatives(
            subject, content, from_email, [participant.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, participant):
        """ Create a JWT token that the user can user to verify its account. """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'participant': participant.email,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return token