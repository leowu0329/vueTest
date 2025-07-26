from django.urls import path
from . import views

app_name = 'cases'

urlpatterns = [
    path('', views.case_list, name='case_list'),
    path('case/<int:pk>/', views.case_detail, name='case_detail'),
    path('case/new/', views.case_create, name='case_create'),
    path('case/<int:pk>/edit/', views.case_update, name='case_update'),
    path('case/<int:pk>/delete/', views.case_delete, name='case_delete'),
    path('api/townships/', views.get_townships, name='get_townships'),
] 