from decimal import Decimal

from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import Customer
from customers.models import Account
from transactions.models import Transaction


@staff_member_required
def admin_dashboard(request):

    total_customers = Customer.objects.count()
    total_accounts = Account.objects.count()
    total_transactions = Transaction.objects.count()

    total_balance = (
        Account.objects.all()
        .aggregate(total=models.Sum("balance"))
        .get("total") or Decimal("0.00")
    )

    pending = Transaction.objects.filter(
        approved=False,
        status="Pending"
    ).order_by("-date")

    context = {
        "customers": total_customers,
        "accounts": total_accounts,
        "transactions": total_transactions,
        "balance": total_balance,
        "pending": pending,
    }

    return render(
        request,
        "admin/dashboard.html",
        context
    )


@staff_member_required
def customer_list(request):

    customers = Customer.objects.select_related("user")

    return render(
        request,
        "admin/customers.html",
        {"customers": customers}
    )


@staff_member_required
def freeze_account(request, id):

    account = get_object_or_404(Account, id=id)

    account.status = "Frozen"
    account.save()

    return redirect("customer_list")


@staff_member_required
def unfreeze_account(request, id):

    account = get_object_or_404(Account, id=id)

    account.status = "Active"
    account.save()

    return redirect("customer_list")


@staff_member_required
def approve_transaction(request, id):

    trx = get_object_or_404(
        Transaction,
        id=id
    )

    # Already processed
    if trx.approved or trx.status != "Pending":
        return redirect("admin_dashboard")

    # Deposit
    if trx.transaction_type == "Deposit":

        if trx.receiver is None:

            trx.status = "Failed"
            trx.save()

            return redirect("admin_dashboard")

        trx.receiver.balance += trx.amount
        trx.receiver.save()

    # Withdrawal
    elif trx.transaction_type == "Withdrawal":

        if trx.sender is None:

            trx.status = "Failed"
            trx.save()

            return redirect("admin_dashboard")

        if trx.sender.balance < trx.amount:

            trx.status = "Failed"
            trx.description = "Insufficient balance"
            trx.save()

            return redirect("admin_dashboard")

        trx.sender.balance -= trx.amount
        trx.sender.save()

    # Approve transaction
    trx.status = "Success"
    trx.approved = True
    trx.save()

    return redirect("admin_dashboard")


@staff_member_required
def daily_report(request):

    today = timezone.now().date()

    transactions = Transaction.objects.filter(
        date__date=today
    ).order_by("-date")

    return render(
        request,
        "admin/daily_report.html",
        {
            "transactions": transactions,
            "today": today,
        }
    )


@staff_member_required
def monthly_report(request):

    month = timezone.now().month
    year = timezone.now().year

    transactions = Transaction.objects.filter(
        date__month=month,
        date__year=year
    ).order_by("-date")

    return render(
        request,
        "admin/monthly_report.html",
        {
            "transactions": transactions,
            "month": month,
            "year": year,
        }
    )