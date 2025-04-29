from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.conf import settings

class User(AbstractUser):
    account_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = str(uuid.uuid4().int)[:10]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=10, unique=True)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"Account {self.account_number} - Balance: {self.balance}"
class reg_details(models.Model):
    username=models.CharField(max_length=150)
    firstname=models.CharField(max_length=150)
    lastname=models.CharField(max_length=150)
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=128, default='default_password')
    def __str__(self):
        return f"reg_details {self.username} -firstname: {self.firstname} - lastname: {self.lastname} - email: {self.email} - password: {self.password}"
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
    ]
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    def __str__(self):
        return f"{self.type} of ${self.amount} on  {self.date.strftime('%Y-%m-%d')} for Account {self.account.account_number}"
