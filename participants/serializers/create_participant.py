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
        subject = f'Completa tu registro @{participant.first_name} {participant.last_name}!'
        from_email = 'OMICHH <noreply@omichh.org>'
        text_content = "este es un contenido en text del correo"
        html_content = f'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body>
                    <h3 style="color: #0091bf; font-weight: bold;">Hola @{ participant.first_name } {participant.last_name}!</h3>
                    <p></p>
                    <p style="color: #2a2a2a; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
                    Tu registro en la Olimpiada Mexicana de informatica casi esta completo, ahora
                    hay que verificar tu cuenta de correo.
                    <br/> Por favor copia y pega esto en tu navegador: <br/> <a style="color:blue;" href="localhost:3000/verify/{verification_token}">localhost:3000/verify/{verification_token}</a>
                    </p>
                </body>
                </html>
            '''
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [participant.email])
        msg.attach_alternative(html_content, "text/html")
        msg.content_subtype = "html"
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