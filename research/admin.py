from django.contrib import admin
from .models import ResearchPublication


@admin.register(ResearchPublication)
class ResearchPublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'authors', 'category', 'publication_year', 'status', 'is_featured', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'publication_year']
    search_fields = ['title', 'authors', 'abstract', 'keywords']
    list_editable = ['status', 'is_featured']
    ordering = ['-created_at']
    actions = ['approve_papers', 'reject_papers']

    def approve_papers(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} papers approved.')
    approve_papers.short_description = 'Approve selected papers'

    def reject_papers(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} papers rejected.')
    reject_papers.short_description = 'Reject selected papers'
