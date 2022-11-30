"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    artist_create_view,
    home_view,
    artist_view,
    artist_list_view,
    info_view,
    login_view,
    logout_view,
    register_view,
    artist_edit_view,
    artist_delete_view,
    get_times_view,
    select_times_view,
    make_appointment_view,
    info_view,
    addPortfolio_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('info/', info_view),
    path('artist/<int:pk>/', artist_view),
    path('artist/', artist_list_view),
    path('artist/create/', artist_create_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('artist/<int:pk>/edit/', artist_edit_view),
    path('artist/<int:pk>/portfolio/', addPortfolio_view),
    path('artist/<int:pk>/delete/', artist_delete_view),
    path('times/<int:pk>/', get_times_view),
    path('times/<int:pk>/appointment/<int:id>/', select_times_view),
    path('times/<int:pk>/appointment/<int:id>/<int:hour>/<int:min>/',
         make_appointment_view),
    path('login/', login_view),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
