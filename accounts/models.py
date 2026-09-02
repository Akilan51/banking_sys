from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    aadhaar = models.CharField(max_length=12)

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username