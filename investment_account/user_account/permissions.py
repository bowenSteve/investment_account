from rest_framework.permissions import BasePermission
from .models import UserInvestmentAccount, Transaction, InvestmentAccount

class IsAllowedToView(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to view the object (Transaction) associated with the investment account.
        """
        # Check if obj is a Transaction or InvestmentAccount
        if isinstance(obj, Transaction):
            # Ensure obj is the investment account
            user_inv_acc = UserInvestmentAccount.objects.filter(
                user=request.user,
                investment_account=obj.investment_account  # Assumes `obj` is a Transaction
            ).first()
            return user_inv_acc and user_inv_acc.can_view
        elif isinstance(obj, InvestmentAccount):
            # Custom logic for InvestmentAccount view permission if needed
            return UserInvestmentAccount.objects.filter(
                user=request.user,
                investment_account=obj,
                can_view=True
            ).exists()
        return False

class IsAllowedToCreate(BasePermission):
    def has_permission(self, request, view):
        """
        Check if the user has permission to create a transaction for a specific investment account.
        """
        investment_account_id = view.kwargs.get('investment_account_pk')
        return request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_create=True
        ).exists()

class IsAllowedToUpdateDelete(BasePermission):
    def has_permission(self, request, view):
        """
        Check if the user has permission to update or delete a transaction for a specific investment account.
        """
        investment_account_id = view.kwargs.get('investment_account_pk')
        if request.method == 'DELETE':
            return request.user.userinvestmentaccount_set.filter(
                investment_account_id=investment_account_id,
                can_delete=True
            ).exists()
        else:
            return request.user.userinvestmentaccount_set.filter(
                investment_account_id=investment_account_id,
                can_update=True
            ).exists()
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # or request.user.is_superuser
