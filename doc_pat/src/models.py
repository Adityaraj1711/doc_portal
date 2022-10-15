import datetime
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models, IntegrityError
from django.utils import timezone


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(verbose_name="Date of birth", blank=True, null=True)
    aadhar = models.CharField(verbose_name="aadhar", max_length=1024, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


salutation_choices = [('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Miss', 'Miss'), ('Dr', 'Dr')]
gender_choice = [('Male', 'Male'), ('Female', 'Female')]
payment_choice = [('T', 'T'), ('FU', 'FU'), ('FOC', 'FOC')]
follow_choice = [(0,0), (10, 10), (15, 15), (20, 20), (30, 30), (45, 45), (60, 60)]

from django.core.exceptions import ValidationError
def only_int(value):
    if value.isdigit()==False:
        raise ValidationError('Enter numbers only')


class Comorbiditie(models.Model):
    comorbiditie = models.CharField(default="", null=False, blank=False, max_length=150)

    def __str__(self):
        return self.comorbiditie


class Procedure(models.Model):
    procedure = models.CharField(default="", null=False, blank=False, max_length=150)

    def __str__(self):
        return self.procedure


class Patient(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    in_time = models.TimeField(default=datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30))
    wait_time = models.CharField(default="0 min", max_length=50, null=True, blank=True)
    seen_by_doctor = models.BooleanField(default=False, editable=False)
    sal = models.CharField(default="Mr.", choices=salutation_choices, max_length=20)
    name = models.CharField(default="", max_length=200, blank=False, null=False)
    age = models.CharField(default="", max_length=10, validators=[only_int], blank=False)
    gender = models.CharField(default="M", max_length=30, choices=gender_choice, null=False, blank=False)
    email_id = models.EmailField(null=True, blank=True)
    address = models.CharField(default="", max_length=200, blank=True, null=True)
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=True, blank=True)
    comorbidities = models.ForeignKey(Comorbiditie, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(default="", max_length=200, null=False, blank=False)
    contact = models.CharField(default="", max_length=14, validators=[only_int])
    referred_by = models.CharField(default="", max_length=50, blank=True, null=True)
    payment_mode = models.CharField(default="Token", choices=payment_choice, null=False, blank=False, max_length=50)
    diagnosis = models.CharField(default="", max_length=1000)
    prescription = models.TextField(default="", null=True, blank=True)
    previous_prescription_data = models.TextField(default="", null=True, blank=True)
    follow_up_days = models.IntegerField(default=10, choices=follow_choice)
    or_days = models.IntegerField(default=0, editable=True, max_length=3)

    def save(self, *args, **kwargs):
        self.follow_up_days = max(self.follow_up_days, self.or_days)
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return self.name + " age: " + str(self.age) + ", gender: " + self.gender

