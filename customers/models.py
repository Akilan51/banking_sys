from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer
import random


ACCOUNT_TYPES = (
    ('Savings', 'Savings'),
    ('Current', 'Current'),
)

STATUS = (
    ('Pending', 'Pending'),
    ('Active', 'Active'),
    ('Frozen', 'Frozen'),
)


def generate_account_number():
    while True:
        number = str(random.randint(100000000000, 999999999999))
        if not Account.objects.filter(account_number=number).exists():
            return number


class Account(models.Model):

    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=12,
        unique=True,
        default=generate_account_number
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPES
    )

    branch = models.CharField(
        max_length=100,
        default="Main Branch"
    )

    ifsc = models.CharField(
        max_length=15,
        default="BANK0001234"
    )

    opening_date = models.DateField(
        auto_now_add=True
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    def __str__(self):
        return f"{self.account_number}"