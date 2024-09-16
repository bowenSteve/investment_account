from django.contrib import admin
from .models import InvestmentAccount, UserInvestmentAccount, Transaction

admin.site.register(InvestmentAccount)
admin.site.register(UserInvestmentAccount)
admin.site.register(Transaction)
