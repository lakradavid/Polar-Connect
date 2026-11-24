from django.db import models


class ResearchStation(models.Model):
    REGION_CHOICES = [
        ('antarctica', 'Antarctica'),
        ('arctic', 'Arctic'),
        ('sub_antarctic', 'Sub-Antarctic'),
        ('sub_arctic', 'Sub-Arctic'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=15, choices=REGION_CHOICES, default='antarctica')
    country = models.CharField(max_length=100, default='India')
    operating_institution = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    established_year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    research_activities = models.TextField(blank=True)
    station_image = models.ImageField(upload_to='stations/images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_demo_data = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MapLocation(models.Model):
    LOCATION_TYPES = [
        ('station', 'Research Station'),
        ('expedition', 'Expedition Site'),
        ('landmark', 'Geographic Landmark'),
        ('sample_site', 'Sample Collection Site'),
    ]

    name = models.CharField(max_length=200)
    location_type = models.CharField(max_length=15, choices=LOCATION_TYPES, default='landmark')
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    research_activities = models.TextField(blank=True)
    image = models.ImageField(upload_to='stations/map/', blank=True, null=True)
    is_demo_data = models.BooleanField(default=True)

    def __str__(self):
        return self.name
