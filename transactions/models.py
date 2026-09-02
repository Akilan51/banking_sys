from django.db import models
from customers.models import Account
import random

TRANSACTION_TYPES = (
    ('Deposit', 'Deposit'),
    ('Withdrawal', 'Withdrawal'),
    ('Transfer', 'Transfer'),
)

STATUS = (
    ('Pending', 'Pending'),
    ('Success', 'Success'),
    ('Failed', 'Failed'),
)

class Transaction(models.Model):

    sender = models.ForeignKey(
        Account,
        related_name='sent',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    receiver = models.ForeignKey(
        Account,
        related_name='received',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    date = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_type


class OTP(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transaction_otps"
    )

    otp = models.CharField(
        max_length=6
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.account.account_number} - {self.otp}"


