from django.db import models
from django.urls import reverse


class Book(models.Model):
   
    title = models.CharField(
        verbose_name="Name",
        max_length=200
    )
    author = models.CharField(
        verbose_name="Author",
        max_length=100
    )
    published_date = models.DateField(
        verbose_name="Date of publication",
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name="Опис",
        blank=True
    )
    cover = models.ImageField(
        verbose_name="Picture",
        upload_to="book_covers/",
        null=True,
        blank=True
    )
    quote = models.TextField(
        verbose_name="Quote",
        blank=True
    )

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('book_detail', args=[str(self.id)])

    def average_rating(self) -> float:
        """
        Calculate and return the average rating for the book, rounded to one decimal.
        If there are no ratings, returns 0.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            total = sum(r.rating for r in ratings)
            count = ratings.count()
            return round(total / count, 1)
        return 0.0


class Rating(models.Model):
    """
    Represents a user-submitted rating for a book, from 1 to 5.
    """
    book = models.ForeignKey(
        Book,
        related_name='ratings',
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="Grade",
        choices=[(i, i) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f"{self.book.title} - {self.rating}"
