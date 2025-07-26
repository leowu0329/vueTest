from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile_edit, name='profile'),
] 