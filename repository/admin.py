from django.contrib import admin
from .models import KnowledgeResource


@admin.register(KnowledgeResource)
class KnowledgeResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'resource_type', 'is_featured', 'is_published', 'download_count', 'created_at']
    list_filter = ['category', 'resource_type', 'is_published', 'is_featured']
    search_fields = ['title', 'author', 'keywords', 'abstract']
    list_editable = ['is_featured', 'is_published']
    ordering = ['-created_at']
