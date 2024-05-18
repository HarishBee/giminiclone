"""
URL configuration for chatg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView
from tp import views



urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/',include('allauth.urls')),
    path('',views.index,name='index'),
    path('skill',views.skill,name='skill'),
    path('register',views.register,name='register'),
    path('educ',views.educ,name='educ'),
    path('activ',views.activ,name='activ'),
    path('login',views.login,name='login'),
    path('verify',views.verify,name='verify'),
    path('home',views.home,name='home'), 
    path('forgot',views.forgot,name='forgot'),
    path('answer',views.answer,name='answer'),
    path('forgot',views.forgot,name='forgot'),
    path('password',views.password,name='password'),
    
    ]
