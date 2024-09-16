from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from django_filters import rest_framework as filters

# Serializer for the InvestmentAccount model
class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = '__all__'

# Serializer for the UserInvestmentAccount model (join table)
class UserInvestmentAccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    investment_account = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserInvestmentAccount
        fields = '__all__'

# Serializer for the Transaction model
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Serializer for the User model (built-in Django user)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TransactionFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Transaction
        fields = ['start_date', 'end_date']

class AdminTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'investment_account', 'transaction_type', 'amount', 'timestamp']

class AdminInvestmentAccountSerializer(serializers.ModelSerializer):
    total_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    transactions = AdminTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = InvestmentAccount
        fields = ['id', 'account_name', 'account_number', 'total_balance', 'transactions']