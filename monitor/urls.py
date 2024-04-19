from django.urls import path
from . import views

urlpatterns = [
    path('speedtest/', views.ClientSpeedTestView.as_view(), name='client-list'),
]