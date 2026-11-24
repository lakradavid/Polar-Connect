from django.contrib import admin
from .models import MediaCategory, MediaAsset


@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'category', 'is_featured', 'allow_download', 'view_count', 'created_at']
    list_filter = ['media_type', 'category', 'is_featured', 'allow_download']
    search_fields = ['title', 'description', 'tags']
    list_editable = ['is_featured', 'allow_download']
