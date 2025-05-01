from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Rating
from django.contrib.auth.models import User

class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Author',
            published_date='2020-01-01',
            description='Desc',
            quote='Quote'
        )

    def test_str(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_get_absolute_url(self):
        url = self.book.get_absolute_url()
        expected = reverse('book_detail', args=[self.book.id])
        self.assertEqual(url, expected)

    def test_average_rating_no_ratings(self):
        self.assertEqual(self.book.average_rating(), 0.0)

    def test_average_rating_with_ratings(self):
        Rating.objects.create(book=self.book, rating=4)
        Rating.objects.create(book=self.book, rating=2)
        self.assertEqual(self.book.average_rating(), 3.0)

class ApiTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.client = APIClient()
        self.book = Book.objects.create(
            title='API Book', author='API Author', published_date='2021-05-01'
        )

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('books', response.data)

    def test_get_books_list(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_get_book_detail(self):
        url = f'/api/books/{self.book.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Book')

    def test_create_book_unauthenticated(self):
        data = {'title': 'New', 'author': 'Auth', 'published_date': '2021-06-01'}
        response = self.client.post('/api/books/', data)
        # DRF returns 403 Forbidden for unauthenticated POST when using IsAuthenticatedOrReadOnly
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rate_book(self):
        rate_url = reverse('submit_rating', args=[self.book.id])
        self.client.login(username='testuser', password='pass')
        response = self.client.post(rate_url, {'rating': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('average_rating', response.json())

class BookOfDayTest(TestCase):
    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.book1 = Book.objects.create(title='Book 1', author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', author='Author 2')

    def test_book_of_day_same_within_day(self):
        response1 = self.client.get(reverse('book_of_the_day'))
        book1 = response1.context['book']
        response2 = self.client.get(reverse('book_of_the_day'))
        book2 = response2.context['book']
        self.assertEqual(book1, book2)

    def test_book_of_day_random_selection(self):
        """Ensure random selection works when cache cleared each time."""
        from django.core.cache import cache
        selections = set()
        for _ in range(20):
            cache.clear()
            response = self.client.get(reverse('book_of_the_day'))
            selections.add(response.context['book'].id)
        self.assertTrue(self.book1.id in selections and self.book2.id in selections)
