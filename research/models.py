from django.db import models
from django.conf import settings


class ResearchPublication(models.Model):
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

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    institution = models.CharField(max_length=200, blank=True)
    abstract = models.TextField()
    keywords = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='antarctic')
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    journal_name = models.CharField(max_length=200, blank=True)
    doi = models.CharField(max_length=100, blank=True, verbose_name='DOI')
    paper_file = models.FileField(upload_to='research/papers/', blank=True, null=True)
    external_link = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to='research/covers/', blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='research_papers'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
