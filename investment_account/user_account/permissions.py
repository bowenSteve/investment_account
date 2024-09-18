from rest_framework.permissions import BasePermission
from .models import UserInvestmentAccount, Transaction, InvestmentAccount

class IsAllowedToView(BasePermission):
    def has_permission(self, request, view):
        investment_account_id = view.kwargs.get('investment_account_pk')
        if not investment_account_id:
            return False
        return request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_view=True
        ).exists()


class IsAllowedToCreate(BasePermission):
    def has_permission(self, request, view):
        investment_account_id = view.kwargs.get('investment_account_pk')
        if not investment_account_id:
            return False
        return request.user.userinvestmentaccount_set.filter(
            investment_account_id=investment_account_id,
            can_create=True
        ).exists()


class IsAllowedToUpdateDelete(BasePermission):
    def has_permission(self, request, view):
        investment_account_id = view.kwargs.get('investment_account_pk')
        if not investment_account_id:
            return False
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




class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  
class DenyViewPermission(BasePermission):
    def has_permission(self, request, view):
        return False
