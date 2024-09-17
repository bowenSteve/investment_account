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

class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    permission_classes = [IsAuthenticated]  

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsAllowedToView()]
        return super().get_permissions()

class UserInvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = UserInvestmentAccount.objects.all()
    serializer_class = UserInvestmentAccountSerializer
    permission_classes = [IsAuthenticated]  


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        investment_account_pk = self.kwargs.get('investment_account_pk')
        if investment_account_pk:
            return Transaction.objects.filter(investment_account_id=investment_account_pk)
        return Transaction.objects.all()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAllowedToView()]
        if self.action == 'create':
            return [IsAllowedToCreate()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAllowedToUpdateDelete()]
        return super().get_permissions()

    def perform_create(self, serializer):
        investment_account_id = self.kwargs.get('investment_account_pk')
        user_inv_acc = UserInvestmentAccount.objects.filter(
            user=self.request.user,
            investment_account_id=investment_account_id,
            can_create=True
        ).first()

        if not user_inv_acc:
            raise serializers.ValidationError("You do not have permission to create transactions for this investment account.")
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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  
class AdminUserTransactionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 

    def get(self, request):
        user = request.user
        investment_accounts = InvestmentAccount.objects.filter(userinvestmentaccount__user=user)
        print(f"Authenticated User: {request.user}")
        
      
        transaction_filter = TransactionFilter(request.GET, queryset=Transaction.objects.filter(investment_account__in=investment_accounts))
        filtered_transactions = transaction_filter.qs
        
   
        total_balance = sum(account.get_total_balance() for account in investment_accounts)

        account_serializer = AdminInvestmentAccountSerializer(investment_accounts, many=True)
        transaction_serializer = AdminTransactionSerializer(filtered_transactions, many=True)
        
        response_data = {
            'total_balance': total_balance,
            'accounts': account_serializer.data,
            'transactions': transaction_serializer.data
        }
        
        return Response(response_data)