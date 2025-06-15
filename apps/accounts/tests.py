from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account, TransactionHistory

User = get_user_model()


class AccountAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password",
            name="tester",
            nickname="testnick",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_account(self):
        url = reverse("accounts:account-create")
        data = {
            "account_number": "1234567890",
            "bank_code": "090",
            "account_type": "SAVING",
        }
        response = self.client.post(url, data)
        print("CREATE ACCOUNT:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_accounts(self):
        Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="090",
            account_type="SAVING",
        )
        url = reverse("accounts:account-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_account(self):
        account = Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="090",
            account_type="SAVING",
        )
        url = reverse("accounts:account-delete", args=[account.account_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TransactionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test2@example.com",
            password="password",
            name="tester2",
            nickname="testnick2",
        )
        self.client.force_authenticate(user=self.user)
        self.account = Account.objects.create(
            user=self.user,
            account_number="1234567899",
            bank_code="090",
            account_type="SAVING",
        )

    def test_create_transaction(self):
        url = reverse("accounts:transaction-create")
        data = {
            "transaction_amount": 10000,
            "description": "test deposit",
            "transaction_details": "ATM",
            "transaction_type": "IN",
            "transaction_method": "TRANSFER",
        }
        response = self.client.post(url, data)
        print("CREATE TRANSACTION:", response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_transactions(self):
        TransactionHistory.objects.create(
            account=self.account,
            transaction_amount=10000,
            description="test",
            transaction_details="ATM",
            transaction_type="IN",
            transaction_method="TRANSFER",
            balance=10000,
        )
        url = reverse("accounts:transaction-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_transaction(self):
        tx = TransactionHistory.objects.create(
            account=self.account,
            transaction_amount=10000,
            description="test",
            transaction_details="ATM",
            transaction_type="IN",
            transaction_method="TRANSFER",
            balance=10000,
        )
        url = reverse("accounts:transaction-update", args=[tx.transaction_id])
        data = {"transaction_amount": 5000, "description": "modified"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "modified")

    def test_delete_transaction(self):
        tx = TransactionHistory.objects.create(
            account=self.account,
            transaction_amount=10000,
            description="test",
            transaction_details="ATM",
            transaction_type="IN",
            transaction_method="TRANSFER",
            balance=10000,
        )
        url = reverse("accounts:transaction-delete", args=[tx.transaction_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
