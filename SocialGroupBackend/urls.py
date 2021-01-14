"""SocialGroupBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from myApp.views import *
from django.views import static
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', EventView.as_view(), name="events"),
    path('activities/', ActivityView.as_view(), name="activities"),
    path('trips/', TripView.as_view(), name="trips"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name="login"),
    path('user-details/', UserDetailsView.as_view(), name="user_details"),
    path('media/avatars/<path>', static.serve, {'document_root': settings.MEDIA_ROOT + '/avatars',}),
]
