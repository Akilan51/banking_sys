from django.db import models
from customers.models import Account


LOAN_STATUS = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
)


class Loan(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    interest = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10
    )

    years = models.PositiveIntegerField()

    emi = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remaining_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        default="Pending"
    )

    applied_on = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.account.account_number}"