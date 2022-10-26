from rest_framework import serializers
from sympy import RootSum
from .models import Appointment, Artist, GetTimes


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('name', 'date', 'time', 'mobile', 'mail')


class CreatAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('name', 'date', 'time', 'mobile', 'mail')


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('host', 'name', 'mobile', 'mail', 'about', 'password')


class CreatArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('name', 'mobile', 'mail', 'about', 'password')
