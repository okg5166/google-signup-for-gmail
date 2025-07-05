from django.urls import path
from gmail_reader import views

urlpatterns = [
    path('', views.home, name='home'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('emails/', views.emails, name='emails'),
] 
