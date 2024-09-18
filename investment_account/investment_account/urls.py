from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_nested import routers
from user_account.views import (
    InvestmentAccountViewSet,
    UserInvestmentAccountViewSet,
    TransactionViewSet,
    UserViewSet, AdminUserTransactionsView
)


router = routers.DefaultRouter()
router.register(r'investment-accounts', InvestmentAccountViewSet, basename='investmentaccount')
router.register(r'user-investment-accounts', UserInvestmentAccountViewSet, basename='userinvestmentaccount')
router.register(r'users', UserViewSet, basename='user')


investment_account_router = routers.NestedDefaultRouter(router, r'investment-accounts', lookup='investment_account')
investment_account_router.register(r'transactions', TransactionViewSet, basename='transactions')


transaction_list = TransactionViewSet.as_view({'get': 'list', 'post': 'create'})
transaction_detail = TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})


urlpatterns = [
    path('admin/user-transactions/<int:user_id>/', AdminUserTransactionsView.as_view(), name='admin-user-transactions'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)), 
    path('', include(investment_account_router.urls)), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('investment-accounts/<int:investment_account_pk>/transactions/', transaction_list, name='transaction-list'),
    path('investment-accounts/<int:investment_account_pk>/transactions/<int:pk>/', transaction_detail, name='transaction-detail'),
]
