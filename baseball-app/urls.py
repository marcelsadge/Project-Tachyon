"""baseapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from data.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash, name = 'splash'),
    path('home/', home, name = 'home'),
    path('login/', login, name='login'),
    path('request_login/', request_login, name='request_login'),
    path('confirm_logout/', confirm_logout, name='confirm_logout'),
    path('logout/', request_logout, name='logout_view'),
    path('register/', register, name='register'),
    path('request_register/', request_register, name='request_register'),
    path('profile/<slug:username>', profile_account, name='profile'),
    path('search/', search, name = 'search'),
    path('create_query/', create_query, name = 'create_query'),
]
