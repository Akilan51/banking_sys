
from django.urls import path
from . import views

urlpatterns = [

    path(
        "deposit/",
        views.deposit,
        name="deposit"
    ),

    path(
        "withdraw/",
        views.withdraw,
        name="withdraw"
    ),

    # OTP URLs
    path(
        "send-otp/",
        views.send_otp,
        name="send_otp"
    ),

    path(
        "verify-otp/",
        views.verify_otp,
        name="verify_otp"
    ),

    path(
        "transfer/",
        views.transfer,
        name="transfer"
    ),

    path(
        "history/",
        views.history,
        name="history"
    ),

    path(
        "statement/",
        views.statement,
        name="statement"
    ),

    path(
        "statement/pdf/",
        views.statement_pdf,
        name="statement_pdf"
    ),
]
