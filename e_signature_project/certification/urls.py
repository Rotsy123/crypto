from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('userlist/', views.get_registered_user, name='get_registered_user')
]
