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

#User Model
User = settings.AUTH_USER_MODEL

MONTH = {
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



class UserManager(BaseUserManager):
    """
    Creates a class to manage the creation of Users.
    """
    def create_user(self, email, full_name, password=None, is_active=True,  is_staff=False, is_admin=False):
        """
        Creates a default user.
        """
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
        """
        Creates a staff user.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name, password=None):
        """
        Creates a super user.
        """
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    """
    Creates a custom user model extending AbstractBaseUser.
    """
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
        """
        String format of user object.
        """
        return self.email

    def get_full_name(self):
        """
        Returns user's full name.
        """
        return self.full_name

    def get_short_name(self):
        """
        Returns user's email.
        """
        return self.email

    @property
    def is_staff(self):
        """
        Returns if the user is a staff.
        """
        return self.staff

    @property
    def is_admin(self):
        """
        Returns if the user is a admin.
        """
        return self.admin

    @property
    def is_active(self):
        """
        Returns if the user is active.
        """
        return self.active

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class GetTimes(models.Model):
    """
    Creates a time object to store the date of appointment.
    """
    date = models.DateField(default=timezone.now, null=False, unique=False)
    name = "Appointment Date"

    def __str__(self):
        """
        Returns the name.
        """
        return self.name

    def getYear(self):
        """
        Returns the year as a int.
        """
        return int(self.date.strftime("%Y"))

    def getMonth(self):
        """
        Returns the month as a int.
        """
        return MONTH[self.date.strftime("%b")]

    def getDay(self):
        """
        Returns the day as a int.
        """
        return int(self.date.strftime("%d"))


class Appointment(models.Model):
    """
    Appointment class
    """
    name = models.CharField(null=False, max_length=20,
                            unique=False, default='')
    date = models.DateField(default=timezone.now, null=False, unique=False)
    time = models.CharField(null=False, unique=False,
                            default='', max_length=5)
    mobile = models.CharField(null=False, default='', max_length=10)
    mail = models.EmailField(null=False)

    def __str__(self):
        """
        Returns the name of the person who made appointment
        """
        return self.name

    def getYear(self):
        """
        Returns the year of the appointment
        """
        return int(self.date.strftime("%Y"))

    def getMonth(self):
        """
        Returns the month of the appointment
        """
        return MONTH[self.date.strftime("%b")]

    def getDay(self):
        """
        Returns the date of the appointment
        """
        return int(self.date.strftime("%d"))

    def getHour(self):
        """
        Returns the hour of the appointment
        """
        return int(self.time[0:self.time.find(":")])

    def getMin(self):
        """
        Returns the minute of the appointment
        """
        return int(self.time[self.time.find(":")+1:])


class Artist(models.Model):
    """
    Artist Class
    """
    creater = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(null=False, max_length=20,
                            unique=False, default='')
    profile = models.ImageField(null=True, blank=True, upload_to="images/")
    mobile = models.CharField(null=False, max_length=10)
    mail = models.EmailField(null=False)
    about = models.TextField(max_length=100)
    json = models.FileField(null=True, blank=True, upload_to="files/")

    def __str__(self):
        """
        Returns the name of the artist
        """
        return self.name

class Portfolio(models.Model):
    """
    Portfolio class to store images
    """
    owner = models.CharField(null=False, max_length=20,
                             unique=False, default='')
    image = models.ImageField(null=True, blank=False, upload_to="images/")
    
    def __str__(self):
        return self.owner
