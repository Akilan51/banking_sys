

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import send_mail

from decimal import Decimal
from datetime import timedelta

from xhtml2pdf import pisa

from customers.models import Account

from .models import Transaction, OTP
from .forms import DepositForm, WithdrawForm, TransferForm




@login_required
def deposit(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":
        form = DepositForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            Transaction.objects.create(
                receiver=account,
                amount=amount,
                transaction_type="Deposit",
                status="Pending"
            )

            messages.success(
                request,
                "Deposit request submitted."
            )

            return redirect("dashboard")

    else:
        form = DepositForm()

    return render(
        request,
        "deposit.html",
        {"form": form}
    )


@login_required
def withdraw(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":
        form = WithdrawForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]

            if account.balance >= amount:
                Transaction.objects.create(
                    sender=account,
                    amount=amount,
                    transaction_type="Withdrawal",
                    status="Pending"
                )

                messages.success(
                    request,
                    "Withdrawal request submitted."
                )

                return redirect("dashboard")

            else:
                messages.error(
                    request,
                    "Insufficient balance."
                )

    else:
        form = WithdrawForm()

    return render(
        request,
        "withdraw.html",
        {"form": form}
    )


@login_required
def transfer(request):

    # Check OTP verification
    if not request.session.get("otp_verified"):
        return redirect("send_otp")

    sender = Account.objects.get(
        customer__user=request.user
    )

    if sender.status != "Active":
        messages.error(
            request,
            "Your account is not active."
        )

        return redirect("dashboard")

    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            receiver_number = form.cleaned_data["account_number"]
            amount = form.cleaned_data["amount"]
            description = form.cleaned_data["description"]

            try:
                receiver = Account.objects.get(
                    account_number=receiver_number
                )

                # Daily transfer limit
                today = timezone.now() - timedelta(days=1)

                daily = Transaction.objects.filter(
                    sender=sender,
                    transaction_type="Transfer",
                    status="Success",
                    date__gte=today
                )

                total = sum(
                    transaction.amount
                    for transaction in daily
                )

                if total + amount > Decimal("50000"):
                    messages.error(
                        request,
                        "Daily transfer limit exceeded."
                    )

                    return redirect("transfer")

                # Balance check
                if sender.balance < amount:
                    Transaction.objects.create(
                        sender=sender,
                        receiver=receiver,
                        amount=amount,
                        transaction_type="Transfer",
                        status="Failed",
                        description="Insufficient Balance"
                    )

                    messages.error(
                        request,
                        "Insufficient Balance"
                    )

                    return redirect("transfer")

                # Transfer money
                sender.balance -= amount
                receiver.balance += amount

                sender.save()
                receiver.save()

                Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    amount=amount,
                    transaction_type="Transfer",
                    description=description,
                    status="Success",
                    approved=True
                )

                # Clear OTP after successful transfer
                request.session["otp_verified"] = False

                messages.success(
                    request,
                    "Money transferred successfully."
                )

                return redirect("dashboard")

            except Account.DoesNotExist:
                messages.error(
                    request,
                    "Receiver account not found."
                )

    else:
        form = TransferForm()

    return render(
        request,
        "transfer.html",
        {"form": form}
    )


@login_required
def send_otp(request):

    account = Account.objects.get(
        customer__user=request.user
    )

    # Generate a new OTP
    code = OTP.generate()

    # Save OTP
    OTP.objects.create(
        account=account,
        otp=code
    )

    # Show OTP in terminal during development
    print("=" * 50)
    print("BANKING SYSTEM OTP")
    print("User:", request.user.username)
    print("Email:", request.user.email)
    print("OTP:", code)
    print("=" * 50)

    # Send email
    send_mail(
        "Bank OTP",
        f"Your OTP is {code}",
        None,
        [request.user.email],
    )

    return redirect("verify_otp")





@login_required
def verify_otp(request):

    account = Account.objects.get(
        customer__user=request.user
    )

    if request.method == "POST":

        code = request.POST.get("otp", "").strip()

        if not code:
            messages.error(
                request,
                "Please enter the OTP."
            )

            return render(
                request,
                "verify_otp.html"
            )

        otp_obj = OTP.objects.filter(
            account=account,
            otp=code
        ).order_by("-created_at").first()

        if otp_obj:

            # Mark OTP as verified
            request.session["otp_verified"] = True

            # Delete used OTP
            otp_obj.delete()

            messages.success(
                request,
                "OTP verified successfully."
            )

            return redirect("transfer")

        messages.error(
            request,
            "Invalid OTP. Please use the latest OTP."
        )

    return render(
        request,
        "verify_otp.html"
    )


@login_required
def history(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    transactions = Transaction.objects.filter(
        Q(sender=account) | Q(receiver=account)
    ).order_by("-date")

    return render(
        request,
        "history.html",
        {
            "transactions": transactions
        }
    )


@login_required
def statement(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    transactions = Transaction.objects.filter(
        Q(sender=account) | Q(receiver=account)
    ).order_by("-date")

    start = request.GET.get("start")
    end = request.GET.get("end")

    if start and end:
        transactions = transactions.filter(
            date__date__range=[start, end]
        )

    context = {
        "transactions": transactions,
        "account": account,
        "start": start,
        "end": end,
    }

    return render(
        request,
        "statement.html",
        context
    )


@login_required
def statement_pdf(request):
    account = Account.objects.get(
        customer__user=request.user
    )

    transactions = Transaction.objects.filter(
        Q(sender=account) | Q(receiver=account)
    ).order_by("-date")

    template = get_template(
        "statement_pdf.html"
    )

    html = template.render({
        "account": account,
        "transactions": transactions,
    })

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="statement.pdf"'
    )

    pisa.CreatePDF(
        html,
        dest=response
    )

    return response
