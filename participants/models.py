from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    """ Adding data to the Base user model """
    CATEGORY = [
        ('OMI','OMI'),
        ('OMIS','OMIS'),
        ('OMIP','OMIP'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.CharField(max_length=150)
    phone = models.PhoneModelField(blank=True)
    category = models.CharField(max_length=4, choices=CATEGORY)
    tutor_name = models.CharField(max_length=100, blank=True, null=True)
    tutor_phone = models.PhoneNumberField(blank=True)
    tutor_email = models.EmailField(max_length=100, blank=True, null=True)




class School(models.Model):
    """ School model """

    name = models.CharField(max_length=250)
    direction = models.CharField(max_length=250)
    principal_name = models.CharField(max_length=150, blank=True, null=True)
    principal_email = models.EmailField(max_length=100, blank=True, null=True)



class Scores(models.Model):
    """ Scores Model Field """

    test = models.IntegerField()
    score = models.IntegerField()