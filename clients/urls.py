from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreateAPIView.as_view(), name='client-list'),
    path('clients/modify/', views.ClientModifyAPIView.as_view(), name='client-detail'),
]
