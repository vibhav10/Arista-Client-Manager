from django.urls import path
from . import views
from . import auth

urlpatterns = [
    path('login/', auth.UserLoginView.as_view(), name='login'),
    path('register/', auth.UserCreationView.as_view(), name='register'),
    path('logout/', auth.UserLogoutView.as_view(), name='logout'),

]