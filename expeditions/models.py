from django.db import models
from django.conf import settings


class Expedition(models.Model):
    REGION_CHOICES = [
        ('antarctica', 'Antarctica'),
        ('arctic', 'Arctic'),
        ('both', 'Both Poles'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    expedition_year = models.PositiveIntegerField()
    region = models.CharField(max_length=15, choices=REGION_CHOICES, default='antarctica')
    location = models.CharField(max_length=200)
    participating_institutions = models.TextField(help_text='One institution per line')
    objectives = models.TextField()
    findings = models.TextField(blank=True)
    chief_scientist = models.CharField(max_length=150, blank=True)
    team_size = models.PositiveIntegerField(null=True, blank=True)
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='expeditions/covers/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_demo_data = models.BooleanField(default=True, help_text='Mark as demonstration data')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-expedition_year']

    def __str__(self):
        return f"{self.name} ({self.expedition_year})"

    def institution_list(self):
        return [i.strip() for i in self.participating_institutions.splitlines() if i.strip()]


class ExpeditionPhoto(models.Model):
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='expeditions/photos/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo for {self.expedition.name}"


class ExpeditionDocument(models.Model):
    expedition = models.ForeignKey(Expedition, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document = models.FileField(upload_to='expeditions/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
