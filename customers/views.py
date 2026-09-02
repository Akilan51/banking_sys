from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import Customer
from .models import Account
from .forms import AccountForm
from transactions.models import Transaction


@login_required
def create_account(request):

    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "phone": "",
            "address": "",
            "aadhaar": "",
        }
    )

    if Account.objects.filter(customer=customer).exists():
        return redirect("dashboard")

    if request.method == "POST":

        form = AccountForm(request.POST)

        if form.is_valid():

            account = form.save(commit=False)

            account.customer = customer

            account.save()

            return redirect("dashboard")

    else:

        form = AccountForm()

    return render(
        request,
        "create_account.html",
        {
            "form": form
        }
    )


@login_required
def dashboard(request):

    # Get Customer profile
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            "phone": "",
            "address": "",
            "aadhaar": "",
        }
    )

    # Get customer's account
    account = Account.objects.filter(
        customer=customer
    ).first()

    # Mini statement
    transactions = []

    if account:

        transactions = Transaction.objects.filter(
            sender=account
        ) | Transaction.objects.filter(
            receiver=account
        )

        transactions = transactions.order_by(
            "-date"
        )[:5]

    return render(
        request,
        "dashboard.html",
        {
            "customer": customer,
            "account": account,
            "transactions": transactions,
        }
    )