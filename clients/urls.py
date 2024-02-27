from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListAPIView.as_view(), name='client-list'),
    path('clients/<int:pk>/', views.ClientDetailAPIView.as_view(), name='client-detail'),
]
