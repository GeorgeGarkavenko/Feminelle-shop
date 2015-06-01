from django.test import TestCase
from django.test.client import Client

class PagesTestsMainPositive(TestCase):

    def test_a_01_home(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_a_02_catalogue(self):
        client = Client()
        response = client.get('/catalogue/')
        self.assertEqual(response.status_code, 200)
   
    def test_a_03_product_class(self):
        client = Client()
        response = client.get('/catalogue/jins')
        self.assertEqual(response.status_code, 200)
        
    def test_a_04_product_all(self):
        client = Client()
        response = client.get('/catalogue/all')
        self.assertEqual(response.status_code, 200)
        
    def test_a_05_product_one_pants(self):
        client = Client()
        response = client.get('/catalogue/pants/1')
        self.assertEqual(response.status_code, 200)
        
    def test_a_06_order(self):
        client = Client()
        response = client.get('/order/')
        self.assertEqual(response.status_code, 200)
        
    def test_a_07_basket(self):
        client = Client()
        response = client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        