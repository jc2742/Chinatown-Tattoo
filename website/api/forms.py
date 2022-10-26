from dataclasses import fields
from random import choices
import django
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from numpy import require
from .models import Artist, Appointment, GetTimes, Portfolio


User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    fullname = forms.CharField()
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password"
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(
                "This is an used email, please pick another.")
        return(email)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password1) <= 8:
            raise forms.ValidationError(
                "Your Password is too short. Needs to be at least 8 characters.")
        if password1 != password2:
            raise forms.ValidationError("Your Password does not match")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "id": "user-password",
            }
        )
    )

    # def clean(self):
    #username = self.cleaned_data_get("username")
    #password = self.cleaned_data_get("password")

    def clean_email(self):
        email = self.cleaned_data.get("email")

        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError(
                "This is an invalid email. Try another email.")
        return(email)


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'name',
            'mobile',
            'mail',
            'about',
            'profile',
            'json'
        ]

    def clean_mobile(self):
        data = self.cleaned_data.get('mobile')
        if len(data) < 9:
            raise forms.ValidationError("This is too short")
        return data


class ArtistEditForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = [
            'name',
            'mobile',
            'mail',
            'about'
        ]

    def save(self, user=None):
        user_profile = super(ArtistForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

    def clean_mobile(self):
        data = self.cleaned_data.get('mobile')
        if len(data) < 10:
            raise forms.ValidationError("This is too short")
        return data


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class TimeForm(forms.ModelForm):
    class Meta:
        model = GetTimes
        fields = [
            'date'
        ]
        widgets = {
            'date': DateInput(),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'name',
            'mobile',
            'mail',
        ]

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = [
            'image'
        ]


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'full_name']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
