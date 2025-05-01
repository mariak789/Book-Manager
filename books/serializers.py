from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'published_date',
            'description',
            'quote',
            'cover',
            'average_rating',
        ]