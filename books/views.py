import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Rating
import random
from datetime import date
from django.core.cache import cache
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import BookForm
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Невірний логін або пароль')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def book_list(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render (request, 'books/book_detail.html', {'book': book})

@require_POST
def submit_rating(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book is not found'}, status=404)
    
    try:
        rating_value = int(request.POST.get('rating', 0))
    except ValueError:
        return JsonResponse({'error': 'Grade should be from 1 to 5.'}, status=400)
    
    Rating.objects.create(book=book, rating=rating_value)
    return JsonResponse({'average_rating': book.average_rating()})

def book_of_the_day(request):
    today = str(date.today())
    book = cache.get(f'book_of_the_day_{today}')

    if not book:
        books = Book.objects.all()
        if books.exists():
            book = random.choice(list(books))
            cache.set(f'book_of_the_day_{today}', book, 60 * 60 * 24)
    return render(request, 'books/book_of_the_day.html', {'book': book})


def is_me(user):
    return user.is_authenticated and user.email == "marusjakarassmaria789@gmail.com" 

@method_decorator(user_passes_test(is_me), name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')

@method_decorator(user_passes_test(is_me), name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book_list')


def home(request):
    return render(request, 'books/home.html')
