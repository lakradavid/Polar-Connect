from django.contrib import admin
from .models import ResearchStation, MapLocation


@admin.register(ResearchStation)
class ResearchStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'country', 'latitude', 'longitude', 'is_active', 'is_demo_data', 'established_year']
    list_filter = ['region', 'country', 'is_active', 'is_demo_data']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_demo_data']


@admin.register(MapLocation)
class MapLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'latitude', 'longitude', 'is_demo_data']
    list_filter = ['location_type', 'is_demo_data']
