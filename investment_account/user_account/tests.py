from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import InvestmentAccount, UserInvestmentAccount, Transaction
from .serializers import AdminTransactionSerializer, AdminInvestmentAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

class InvestmentAccountAPITestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='password123')

   
        self.inv_acc1 = InvestmentAccount.objects.create(account_name='Account 1', account_number='1234567890', balance=1000)
        self.inv_acc2 = InvestmentAccount.objects.create(account_name='Account 2', account_number='0987654321', balance=2000)

     
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.inv_acc1, can_view=True)
        UserInvestmentAccount.objects.create(user=self.user2, investment_account=self.inv_acc2, can_create=True, can_update=True, can_delete=True)
        UserInvestmentAccount.objects.create(user=self.user1, investment_account=self.inv_acc2, can_create=True)

      
        self.transaction1 = Transaction.objects.create(investment_account=self.inv_acc1, transaction_type='deposit', amount=500)
        self.transaction2 = Transaction.objects.create(investment_account=self.inv_acc2, transaction_type='withdrawal', amount=300)
        
        
        self.user1_token = str(RefreshToken.for_user(self.user1).access_token)
        self.user2_token = str(RefreshToken.for_user(self.user2).access_token)
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)

    def test_user_can_view_investment_account(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get(f'/investment-accounts/{self.inv_acc1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_cannot_create_transaction_without_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.post(f'/investment-accounts/{self.inv_acc1.id}/transactions/', data={
            'transaction_type': 'deposit',
            'amount': 200
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_transaction_with_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.post(f'/investment-accounts/{self.inv_acc2.id}/transactions/', data={
            'investment_account': self.inv_acc2.id,  
            'transaction_type': 'deposit',
            'amount': 300
            }, format='json')
        print(response.data) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_admin_can_get_user_transactions_with_date_range(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        start_date = timezone.now() - timedelta(days=7)
        end_date = timezone.now() + timedelta(days=1)
        response = self.client.get('/admin/user-transactions/', data={
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_balance', response.data)
        self.assertIn('accounts', response.data)
        self.assertIn('transactions', response.data)
    
    def test_user_cannot_access_admin_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user1_token}')
        response = self.client.get('/admin/user-transactions/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
