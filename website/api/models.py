from pyexpat import model
from sqlite3 import Timestamp
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager
)

from django.conf import settings
from datetime import datetime
# Create your models here.

User = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True,  is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("User must have a full name")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class GetTimes(models.Model):
    date = models.DateField(default=timezone.now, null=False, unique=False)
    name = "Time"

    def __str__(self):
        return self.name

    def getYear(self):
        return int(self.date.strftime("%Y"))

    def getMonth(self):
        month = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }

        return month[self.date.strftime("%b")]

    def getDay(self):
        return int(self.date.strftime("%d"))


class Appointment(models.Model):
    name = models.CharField(null=False, max_length=20,
                            unique=False, default='')
    date = models.DateField(default=timezone.now, null=False, unique=False)
    time = models.CharField(null=False, unique=False,
                            default='', max_length=5)
    mobile = models.CharField(null=False, default='', max_length=10)
    mail = models.EmailField(null=False)

    def __str__(self):
        return self.name

    def getYear(self):
        return int(self.date.strftime("%Y"))

    def getMonth(self):
        month = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "June": 6,
            "July": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }

        return month[self.date.strftime("%b")]

    def getDay(self):
        return int(self.date.strftime("%d"))

    def getHour(self):
        return int(self.time[0:self.time.find(":")])

    def getMin(self):
        return int(self.time[self.time.find(":")+1:])


class Artist(models.Model):
    creater = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(null=False, max_length=20,
                            unique=False, default='')
    profile = models.ImageField(null=True, blank=True, upload_to="images/")
    mobile = models.CharField(null=False, max_length=10)
    mail = models.EmailField(null=False)
    about = models.TextField(max_length=100)
    json = models.FileField(null=True, blank=True, upload_to="files/")

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    owner = models.CharField(null=False, max_length=20,
                             unique=False, default='')
    image = models.ImageField(null=True, blank=False, upload_to="images/")
    
    def __str__(self):
        return self.owner
