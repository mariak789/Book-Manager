import json
import random
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from rest_framework import viewsets

from .models import Book, Rating
from .forms import BookForm, UserRegistrationForm, UserLoginForm
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'books/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                auth_login(request, user)
                return redirect('book_list')
            form.add_error(None, 'Невірний логін або пароль')
    else:
        form = UserLoginForm()
    return render(request, 'books/login.html', {'form': form})


def book_list(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@require_POST
def submit_rating(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        rating_value = int(request.POST.get('rating', 0))
    except ValueError:
        return JsonResponse({'error': 'Grade should be from 1 to 5.'}, status=400)
    Rating.objects.create(book=book, rating=rating_value)
    return JsonResponse({'average_rating': book.average_rating()})


def book_of_the_day(request):
    today = date.today().isoformat()
    cache_key = f'book_of_the_day_{today}'
    book = cache.get(cache_key)
    if not book:
        books = Book.objects.all()
        if books.exists():
            book = random.choice(list(books))
            cache.set(cache_key, book, 24 * 3600)
    return render(request, 'books/book_of_the_day.html', {'book': book})


def is_admin_user(user):
    return user.is_authenticated and user.is_staff


@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')


@method_decorator(user_passes_test(is_admin_user), name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')


def home(request):
    return render(request, 'books/home.html')