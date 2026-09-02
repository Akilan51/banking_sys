from django.urls import path
from . import views


urlpatterns = [

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "customers/",
        views.customer_list,
        name="customer_list"
    ),

    path(
        "account/<int:id>/freeze/",
        views.freeze_account,
        name="freeze_account"
    ),

    path(
        "account/<int:id>/unfreeze/",
        views.unfreeze_account,
        name="unfreeze_account"
    ),

    path(
        "transaction/<int:id>/approve/",
        views.approve_transaction,
        name="approve_transaction"
    ),

    path(
        "daily-report/",
        views.daily_report,
        name="daily_report"
    ),

    path(
        "monthly-report/",
        views.monthly_report,
        name="monthly_report"
    ),
]