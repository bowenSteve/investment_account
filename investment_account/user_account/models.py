from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class InvestmentAccount(models.Model):
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_name

    def get_total_balance(self):
        return self.transaction_set.aggregate(Sum('amount'))['amount__sum'] or 0

class UserInvestmentAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)

    can_view = models.BooleanField(default=False)   
    can_create = models.BooleanField(default=False)  
    can_update = models.BooleanField(default=False)  
    can_delete = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('user', 'investment_account')

    def __str__(self):
        return f"{self.user.username} - {self.investment_account.account_name}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    )

    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.investment_account.account_name}"
