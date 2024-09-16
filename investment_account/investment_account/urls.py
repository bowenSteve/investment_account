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

# Main router for base resources
router = routers.DefaultRouter()
router.register(r'investment-accounts', InvestmentAccountViewSet, basename='investmentaccount')
router.register(r'user-investment-accounts', UserInvestmentAccountViewSet, basename='userinvestmentaccount')
router.register(r'users', UserViewSet, basename='user')

# Nested router for transactions under investment accounts
investment_account_router = routers.NestedDefaultRouter(router, r'investment-accounts', lookup='investment_account')
investment_account_router.register(r'transactions', TransactionViewSet, basename='transactions')

# Custom views for transactions (if you want to handle specific methods outside of the router)
transaction_list = TransactionViewSet.as_view({'get': 'list', 'post': 'create'})
transaction_detail = TransactionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})

# URL Patterns
urlpatterns = [
    path('admin/user-transactions/', AdminUserTransactionsView.as_view(), name='admin-user-transactions'),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Include base router URLs
    path('', include(investment_account_router.urls)),  # Include nested router URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    
    # Custom routes for transactions if needed
    path('investment-accounts/<int:investment_account_pk>/transactions/', transaction_list, name='transaction-list'),
    path('investment-accounts/<int:investment_account_pk>/transactions/<int:pk>/', transaction_detail, name='transaction-detail'),
]
