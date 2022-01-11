from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Participant(models.Model):
    """ Adding data to the Base user model """
    CATEGORY = [
        ('OMI','OMI'),
        ('OMIS','OMIS'),
        ('OMIP','OMIP'),
    ]
    TYPE = [
        ('student','alumno'),
        ('teacher', 'maestro'),
    ]
    type_of_participant = models.CharField(max_length=50, choices=TYPE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    temp_user_name_omegaup = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.CharField(max_length=150)
    phone = PhoneNumberField(blank=True)
    town = models.CharField(max_length=150)
    category = models.CharField(max_length=4, choices=CATEGORY)
    tutor_name = models.CharField(max_length=100, blank=True, null=True)
    tutor_phone = PhoneNumberField(blank=True)
    tutor_email = models.EmailField(max_length=100, blank=True, null=True)

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class School(models.Model):
    """ School model """

    name = models.CharField(max_length=250)
    direction = models.CharField(max_length=250)
    principal_name = models.CharField(max_length=150, blank=True, null=True)
    principal_email = models.EmailField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Scores(models.Model):
    """ Scores Model Field """

    test = models.IntegerField()
    score = models.IntegerField()

    def __str__ (self):
        return self.score