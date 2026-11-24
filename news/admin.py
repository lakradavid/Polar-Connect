from django.contrib import admin
from .models import NewsCategory, NewsArticle, Event


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'status', 'is_featured', 'view_count', 'published_at']
    list_filter = ['status', 'category', 'is_featured']
    search_fields = ['title', 'summary', 'content']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['publish_articles']

    def publish_articles(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{queryset.count()} articles published.')
    publish_articles.short_description = 'Publish selected articles'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_datetime', 'is_online', 'is_featured']
    list_filter = ['event_type', 'is_online', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured']
