from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from customers.models import Account
from .models import OTP, Beneficiary
from .forms import BeneficiaryForm


@login_required
def send_otp(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    code = OTP.generate()

    OTP.objects.create(
        account=account,
        otp=code
    )

    send_mail(
        "Bank OTP",
        f"Your OTP is {code}",
        None,
        [request.user.email]
    )

    return redirect("verify_otp")


@login_required
def verify_otp(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":
        code = request.POST["otp"]

        obj = OTP.objects.filter(
            account=account,
            otp=code
        ).last()

        if obj:
            request.session["otp_verified"] = True
            return redirect("transfer")

    return render(request, "verify_otp.html")


@login_required
def beneficiaries(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    data = Beneficiary.objects.filter(
        account=account
    )

    return render(
        request,
        "beneficiaries.html",
        {"beneficiaries": data}
    )


@login_required
def add_beneficiary(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":
        form = BeneficiaryForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.account = account
            obj.save()

            return redirect("beneficiaries")

    else:
        form = BeneficiaryForm()

    return render(
        request,
        "beneficiary_add.html",
        {"form": form}
    )