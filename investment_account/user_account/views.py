from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from .serializers import (
    InvestmentAccountSerializer,
    UserInvestmentAccountSerializer,
    TransactionSerializer,
    UserSerializer, AdminInvestmentAccountSerializer, AdminTransactionSerializer, TransactionFilter

)
from .permissions import IsAllowedToView, IsAllowedToCreate, IsAllowedToUpdateDelete, IsAdmin

# ViewSet for the InvestmentAccount model
class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

    def get_permissions(self):
        if self.action == 'retrieve':
            # Check view permission
            return [IsAuthenticated(), IsAllowedToView()]
        return super().get_permissions()

# ViewSet for the UserInvestmentAccount model (join table)
class UserInvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = UserInvestmentAccount.objects.all()
    serializer_class = UserInvestmentAccountSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in

# ViewSet for the Transaction model
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Base authentication requirement

    def get_queryset(self):
        """
        Override get_queryset to filter transactions by investment account.
        """
        investment_account_pk = self.kwargs.get('investment_account_pk')
        if investment_account_pk:
            return Transaction.objects.filter(investment_account_id=investment_account_pk)
        return Transaction.objects.all()

    def get_permissions(self):
        """
        Set different permissions based on action.
        """
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAllowedToView()]
        if self.action == 'create':
            return [IsAllowedToCreate()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAllowedToUpdateDelete()]
        return super().get_permissions()

    def perform_create(self, serializer):
        investment_account_id = self.kwargs.get('investment_account_pk')
        # Validate user permissions
        user_inv_acc = UserInvestmentAccount.objects.filter(
            user=self.request.user,
            investment_account_id=investment_account_id,
            can_create=True
        ).first()

        if not user_inv_acc:
            raise serializers.ValidationError("You do not have permission to create transactions for this investment account.")
        
        # Save the transaction with the correct investment account
        serializer.save(investment_account_id=investment_account_id)

class IsAllowedToCreate(BasePermission):
    def has_permission(self, request, view):
        investment_account_id = view.kwargs.get('investment_account_pk')
        return request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_create=True
        ).exists()

class IsAllowedToUpdateDelete(BasePermission):
    def has_permission(self, request, view):
        investment_account_id = view.kwargs.get('investment_account_pk')
        return request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_update=True
        ).exists() or request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_delete=True
        ).exists()

# ViewSet for the User model (built-in Django user)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is logged in
class AdminUserTransactionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Ensure only authenticated admins can access

    def get(self, request):
        user = request.user
        investment_accounts = InvestmentAccount.objects.filter(userinvestmentaccount__user=user)
        print(f"Authenticated User: {request.user}")
        
        # Apply date range filter to transactions
        transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(investment_account__in=investment_accounts))
        filtered_transactions = transaction_filter.qs
        
        # Calculate total balance across all accounts
        total_balance = sum(account.get_total_balance() for account in investment_accounts)
        
        # Serialize the data
        account_serializer = AdminInvestmentAccountSerializer(investment_accounts, many=True)
        transaction_serializer = AdminTransactionSerializer(filtered_transactions, many=True)
        
        response_data = {
            'total_balance': total_balance,
            'accounts': account_serializer.data,
            'transactions': transaction_serializer.data
        }
        
        return Response(response_data)