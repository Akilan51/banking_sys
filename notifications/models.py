from django.db import models
from customers.models import Account
import random

class Beneficiary(models.Model):

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="beneficiaries"
    )

    beneficiary_name = models.CharField(max_length=100)

    beneficiary_account = models.CharField(max_length=20)

    beneficiary_ifsc = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.beneficiary_name



class OTP(models.Model): 
    account = models.ForeignKey( Account, on_delete=models.CASCADE, related_name="notification_otps" )
    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate():

        return str(random.randint(100000,999999))