from django.test import TestCase
from django.test.client import Client

class PagesTestsInfoPositive(TestCase):

    def test_b_01_news(self):
        client = Client()
        response = client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_b_02_news_item(self):
        client = Client()
        response = client.get('/news/1')
        self.assertEqual(response.status_code, 200)

    def test_b_03_reviews(self):
        client = Client()
        response = client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
 
    def test_b_04_review(self):
        client = Client()
        response = client.get('/reviews/1')
        self.assertEqual(response.status_code, 200)
 
    def test_b_05_articles(self):
        client = Client()
        response = client.get('/articles/')
        self.assertEqual(response.status_code, 200)
 
    def test_b_06_size_tables(self):
        client = Client()
        response = client.get('/articles/sizes_table')
        self.assertEqual(response.status_code, 200)
 
    def test_b_07_articles_arbitrary(self):
        client = Client()
        response = client.get('/articles/pregnancy_test-')
        self.assertEqual(response.status_code, 200)
 
    def test_b_08_contact(self):
        client = Client()
        response = client.get('/contact/')
        self.assertEqual(response.status_code, 200)
 
    def test_b_09_history(self):
        client = Client()
        response = client.get('/history/')
        self.assertEqual(response.status_code, 200)
 
    def test_b_10_sitemap(self):
        client = Client()
        response = client.get('/sitemap/')
        self.assertEqual(response.status_code, 200)
 