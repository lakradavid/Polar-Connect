from django.db import models
from django.conf import settings


class MediaCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Media Categories'

    def __str__(self):
        return self.name


class MediaAsset(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('embed', 'Embedded Video'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    category = models.ForeignKey(MediaCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    image = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    embed_url = models.URLField(blank=True, help_text='YouTube or Vimeo embed URL')
    tags = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    photographer = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=200, blank=True)
    taken_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    allow_download = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='media_uploads'
    )
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]
