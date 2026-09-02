from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.apply_loan, name="apply_loan"),
    path("", views.loan_list, name="loan_list"),
    path("approve/<int:id>/", views.approve_loan, name="approve_loan"),
    path("pay/<int:id>/", views.pay_emi, name="pay_emi"),
]

