from django.contrib import admin
from django.utils.html import format_html
from .models import Book, Rating


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'cover_preview')
    list_filter = ('published_date',)
    search_fields = ('title', 'author')
    readonly_fields = ('cover_preview',)
    fields = ('title', 'author', 'published_date', 'description', 'quote', 'cover', 'cover_preview')

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="max-height: 200px;">', obj.cover.url)
        return "—"
    cover_preview.short_description = "Обкладинка"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title',)
    ordering = ('-created_at',)