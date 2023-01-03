from django.shortcuts import render, redirect
from html5lib import serialize
from requests import post
from rest_framework import generics, status
from .models import Appointment, Artist, Portfolio, UserManager, User, GetTimes
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ArtistForm, LoginForm, RegisterForm, AppointmentForm, ArtistEditForm, TimeForm, PortfolioForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django import forms
from .CalFunc import returnTimes, makeAppointment
from async_timeout import timeout


# Create your views here.

User = get_user_model()


def home_view(request, *args, **kawrgs):
    """
    Displays the landing page
    """
    return render(request, "home.html", {})

def info_view(request, *args, **kawrgs):
    """
    Displays the info page
    """
    return render(request, "info.html", {})

@login_required
def artist_create_view(request, *args, **kwargs):
    """
    Displays a form to create an artist
    """
    form = ArtistForm(request.POST, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.creater = request.user
        obj.save()
        form = ArtistForm()
        return redirect('/artist/')
    return render(request, "form.html", {"form": form, "title": "Add New Artist"})


def artist_list_view(request, *args, **kwargs):
    """
    Displays all artists
    """
    qs = Artist.objects.all()
    context = {"artist_list": qs}
    context["pfp"] = []

    return render(request, "list.html", context)


def get_times_view(request, pk, *args, **kwargs):
    """
    Displays a page to dates for appointment
    """
    form = TimeForm(request.POST or None)
    file = Artist.objects.get(pk=pk)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = TimeForm()
        return redirect(f'appointment/{obj.id}/')
    return render(request, "form.html", {"form": form, "title": "Select Date For Appointment"})


def select_times_view(request, pk, id, *args, **kwargs):
    """
    Displays all available times artist is free for appointment
    """
    file = Artist.objects.filter(id=pk).first()
    print(len(str(file.json)))
    if len(str(file.json)) is 0:
        return render(request, "error.html", {"error": "Artist is not available to make consulting appointments!"})
    obj = GetTimes.objects.get(id=id)
    form = returnTimes(obj.getYear(), obj.getMonth(), obj.getDay(), file.json)
    return render(request, "times.html", {"times": form})


def make_appointment_view(request, pk, id, hour, min, * args, **kwargs):
    """
    Displays a form to create an appointment
    """
    form = AppointmentForm(request.POST or None)
    if form.is_valid():
        file = Artist.objects.get(pk=pk)
        obj = form.save(commit=False)
        obj.date = GetTimes.objects.get(id=id).date
        obj.time = f'{hour}:{min}'
        obj.save()
        makeAppointment(obj.getYear(), obj.getMonth(), obj.getDay(), obj.getHour(), obj.getMin(), obj.mail, obj.name, obj.mobile, file.json)
        form = AppointmentForm()
        return redirect('/')
    return render(request, "form.html", {"form": form, "title": "Create An Appointment"})


def artist_view(request, pk, *args, **kwargs):
    """
    Displays an artist page
    """
    try:
        obj = Artist.objects.get(pk=pk)
    except Artist.DoesNotExist:
        raise Http404
    qs = Portfolio.objects.filter(owner=obj.name)
    context = {
        "name": obj.name,
        "mail": obj.mail,
        "mobile": obj.mobile,
        "about": obj.about,
        "image": obj.profile,
        "portfolio":qs,
        "id":pk,
    }
    return render(request, "account.html", context)


def addPortfolio_view(request, pk, *args, **kwargs):
    """
    Displays a form for artist to add pictures
    """
    form = PortfolioForm(request.POST, request.FILES or None)
    if form.is_valid():
        name = Artist.objects.get(pk=pk)
        obj = form.save(commit=False)
        obj.owner = name.name
        obj.save()
        return redirect(f"/artist/{pk}/")
    return render(request, "form.html", {"form": form, "title": "Add Pictures"})


@ login_required
def artist_edit_view(request, pk, *args, **kwargs):
    """
    Displays a form to edit a current artist
    """
    context = {}
    obj = Artist.objects.get(id=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, request.FILES or None, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(f"/artist/{pk}/")
    else:
        form = ArtistForm(request.FILES or None, instance=obj)
    context["artist"] = obj
    context["form"] = form
    context["title"] = obj.name
    return render(request, "updateArtist.html", context)


@ login_required
def artist_delete_view(request, pk):
    """
    Deletes an artist
    """
    obj = Artist.objects.get(pk=pk)
    obj.delete()
    return redirect('/artist/')

@ login_required
def artist_pic_view(request, pk):
    """
    Veiws all the picture the artist has
    """
    obj = Artist.objects.get(pk=pk)
    qs = Portfolio.objects.filter(owner=obj.name)
    context={
        "name":obj.name,
        "mail": obj.mail,
        "mobile": obj.mobile,
        "about": obj.about,
        "image": obj.profile,
        "portfolio":qs,
        "id":obj.id,
    }
    return render(request,"images.html", context)

@ login_required
def artist_delete_pic_view(request,pk,img_id):
    """
    Deletes a picture from the artist porfolio
    """
    obj = Portfolio.objects.get(id=img_id)
    obj.delete()
    return redirect(f'/artist/{pk}/')


@ login_required
def register_view(request, *args, **kwargs):
    """
    Displays a form to register an staff user
    """
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        fullname = form.cleaned_data.get("fullname")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_staffuser(
                email, full_name=fullname, password=password)
        except:
            user = None
        if user != None:
            return redirect("/artist/")
        else:
            request.session['register_error'] = 1

    return render(request, "form.html", {"form": form, "title": "Register Artist"})


def login_view(request):
    """
    Displays a form to login
    """
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("/artist/")
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        userr = authenticate(request, email=email, password=password)
        if userr != None:
            login(request, userr)
            return redirect("/artist/")
        else:
            # attempt = request.session.get("attempt") or 0
            # request.session["attempt"] = attempt + 1}
            request.session['invalid_user'] = 1

    return render(request, "form.html", {"form": form, "title": "Login"})


def logout_view(request):
    """
    Logouts out a user
    """
    logout(request)
    return redirect("/")
