import os
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'excel.settings')


class SpreadsheetAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user)
        self.access_token = str(self.token.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_and_retrieve_cell(self):
        response = self.client.post(
            reverse(
                'sheets:cell-create-retrieve',
                args=['sheet1', 'A1']
            ),
            {'value': '42'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('sheets:cell-create-retrieve', args=['sheet1', 'A1']), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], '42')

    def test_calculate_formula(self):
        self.client.post(reverse('sheets:cell-create-retrieve', args=['sheet1', 'A1']), {'value': '5'}, format='json')
        self.client.post(reverse('sheets:cell-create-retrieve', args=['sheet1', 'A2']), {'value': '7'}, format='json')

        response = self.client.post(
            reverse(
                'sheets:cell-create-retrieve',
                args=['sheet1', 'A3']
            ),
            {'value': '=A1+A2'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(reverse('sheets:cell-create-retrieve', args=['sheet1', 'A3']), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], '=A1+A2')
        self.assertEqual(response.data['result'], '12')

    def test_sheet_data(self):
        self.client.post(
            reverse(
                'sheets:cell-create-retrieve',
                args=['sheet2', 'A1']
            ),
            {'value': '1'},
            format='json'
        )
        self.client.post(
            reverse(
                'sheets:cell-create-retrieve',
                args=['sheet2', 'A2']
            ),
            {'value': '2'},
            format='json'
        )
        self.client.post(
            reverse(
                'sheets:cell-create-retrieve',
                args=['sheet2', 'A3']
            ),
            {'value': '=A1+A2'},
            format='json'
        )

        response = self.client.get(reverse('sheets:sheet-data', args=['sheet2']), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data['A1']['value'], '1')
        self.assertEqual(response.data['A2']['value'], '2')
        self.assertEqual(response.data['A3']['value'], '=A1+A2')
