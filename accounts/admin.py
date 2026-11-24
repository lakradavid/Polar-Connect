from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Notification, Bookmark


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'full_name', 'user_category', 'role', 'date_joined', 'is_active']
    list_filter = ['user_category', 'role', 'is_active', 'is_staff']
    search_fields = ['email', 'username', 'full_name', 'institution']
    ordering = ['-date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('PolarConnect Profile', {'fields': ('full_name', 'phone_number', 'institution', 'designation', 'user_category', 'role', 'bio', 'profile_picture', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PolarConnect Profile', {'fields': ('email', 'full_name', 'user_category', 'role')}),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['user__email', 'title']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'object_id', 'created_at']
    list_filter = ['content_type']
