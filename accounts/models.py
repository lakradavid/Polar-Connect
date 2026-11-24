from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_CATEGORIES = [
        ('student', 'Student'),
        ('researcher', 'Researcher'),
        ('educator', 'Educator'),
        ('scientific_professional', 'Scientific Professional'),
        ('general_public', 'General Public'),
    ]

    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('content_admin', 'Content Administrator'),
        ('researcher', 'Researcher'),
        ('educator', 'Educator'),
        ('student', 'Student'),
        ('general_user', 'General User'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    user_category = models.CharField(max_length=30, choices=USER_CATEGORIES, default='general_public')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='general_user')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined_platform = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_display_name(self):
        return self.full_name or self.username

    @property
    def is_admin_role(self):
        return self.role in ('super_admin', 'content_admin') or self.is_staff

    @property
    def is_researcher_role(self):
        return self.role == 'researcher'


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('research', 'New Research Published'),
        ('education', 'New Educational Material'),
        ('event', 'Upcoming Event'),
        ('announcement', 'Announcement'),
        ('community', 'Community Reply'),
        ('approved', 'Content Approved'),
        ('general', 'General'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} – {self.title}"


class Bookmark(models.Model):
    CONTENT_TYPES = [
        ('research', 'Research Paper'),
        ('resource', 'Knowledge Resource'),
        ('news', 'News Article'),
        ('expedition', 'Expedition'),
        ('media', 'Media Asset'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookmarks')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.content_type}:{self.object_id}"
