from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from customers.models import Account
from .models import Loan
from .forms import LoanForm


@login_required
def apply_loan(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":
        form = LoanForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)

            loan.account = account

            principal = loan.amount

            rate = loan.interest / Decimal("1200")

            months = loan.years * 12

            # Handle 0% interest
            if rate == 0:
                emi = principal / months
            else:
                emi = (
                    principal * rate * (1 + rate) ** months
                ) / (
                    (1 + rate) ** months - 1
                )

            loan.emi = round(emi, 2)

            loan.remaining_amount = principal

            loan.status = "Pending"

            loan.save()

            return redirect("loan_list")

    else:
        form = LoanForm()

    return render(
        request,
        "loan_apply.html",
        {"form": form}
    )


@login_required
def loan_list(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    loans = Loan.objects.filter(
        account=account
    ).order_by("-id")

    return render(
        request,
        "loan_list.html",
        {"loans": loans}
    )


@staff_member_required
def approve_loan(request, id):
    loan = get_object_or_404(
        Loan,
        id=id
    )

    # Don't approve an already processed loan
    if loan.status != "Pending":
        return redirect("admin_dashboard")

    loan.status = "Approved"
    loan.save()

    loan.account.balance += loan.amount
    loan.account.save()

    return redirect("admin_dashboard")


@login_required
def pay_emi(request, id):
    loan = get_object_or_404(
        Loan,
        id=id
    )

    account = loan.account

    # EMI can only be paid for approved loans
    if loan.status != "Approved":
        return redirect("loan_list")

    # Check balance
    if account.balance >= loan.emi:
        account.balance -= loan.emi
        account.save()

        loan.remaining_amount -= loan.emi

        if loan.remaining_amount <= 0:
            loan.remaining_amount = Decimal("0.00")
            loan.status = "Completed"

        loan.save()

    return redirect("loan_list")

