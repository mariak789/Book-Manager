from django.urls import path
from . import views
from .views import BookCreateView, BookUpdateView


urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/rate/', views.submit_rating, name='submit_rating'),
    path('book-of-the-day/', views.book_of_the_day, name='book_of_the_day'),
    path('add/', BookCreateView.as_view(), name='book_add'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'), 
]