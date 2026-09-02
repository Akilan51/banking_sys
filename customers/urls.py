from django.urls import path
from . import views

urlpatterns = [

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'create-account/',
        views.create_account,
        name='create_account'
    ),

]