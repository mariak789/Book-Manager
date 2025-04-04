from django.db import models
from django.urls import reverse

class Book(models.Model):
    title = models.CharField("Name", max_length=200)
    author = models.CharField("Author", max_length=100)
    published_date = models.DateField("Date of publication", null=True, blank=True)
    description = models.TextField("Опис", blank=True)
    cover = models.ImageField("Picture", upload_to="book_covers/", null=True, blank=True)
    quote = models.TextField("Quote", blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg = sum(r.rating for r in ratings) / ratings.count()
            return round(avg, 1)
        return 0


class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField("Grade", choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.rating}"
