from django.db import models
from django.conf import settings


class KnowledgeResource(models.Model):
    CATEGORY_CHOICES = [
        ('antarctic', 'Antarctic Research'),
        ('arctic', 'Arctic Research'),
        ('climate_change', 'Climate Change'),
        ('glaciology', 'Glaciology'),
        ('marine_biology', 'Marine Biology'),
        ('polar_ecology', 'Polar Ecology'),
        ('atmospheric', 'Atmospheric Science'),
        ('oceanography', 'Oceanography'),
        ('geology', 'Geology'),
        ('polar_technology', 'Polar Technology'),
    ]

    RESOURCE_TYPES = [
        ('pdf', 'PDF Document'),
        ('report', 'Research Report'),
        ('article', 'Scientific Article'),
        ('educational', 'Educational Document'),
        ('data', 'Dataset'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    abstract = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True, help_text='Comma-separated keywords')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='antarctic')
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='pdf')
    publication_date = models.DateField(null=True, blank=True)
    uploaded_file = models.FileField(upload_to='documents/', blank=True, null=True)
    external_url = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='repository/thumbnails/', blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='uploaded_resources'
    )
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def keyword_list(self):
        return [k.strip() for k in self.keywords.split(',') if k.strip()]
