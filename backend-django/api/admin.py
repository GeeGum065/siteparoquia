from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'data', 'created_at']
    list_filter = ['categoria', 'data', 'created_at']
    search_fields = ['titulo', 'texto']
    date_hierarchy = 'data'
    ordering = ['-data']
