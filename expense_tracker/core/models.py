from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20)
    date = models.DateField()
    payment_mode = models.CharField(max_length=20)
    notes = models.CharField(max_length=200, blank=True, null=True)
    is_shared = models.BooleanField(default=False)

class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')

class Repayment(models.Model):
    payer = models.ForeignKey(User, related_name='payer', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    month = models.CharField(max_length=7)
    amount = models.DecimalField(max_digits=10, decimal_places=2)