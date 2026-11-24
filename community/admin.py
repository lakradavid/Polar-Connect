from django.contrib import admin
from .models import DiscussionForum, Discussion, Comment


@admin.register(DiscussionForum)
class DiscussionForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'forum', 'author', 'status', 'view_count', 'created_at']
    list_filter = ['status', 'forum', 'is_question']
    search_fields = ['title', 'content']
    list_editable = ['status']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'author', 'is_answer', 'is_moderated', 'created_at']
    list_filter = ['is_answer', 'is_moderated']
    list_editable = ['is_moderated']
