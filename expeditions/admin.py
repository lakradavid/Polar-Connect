from django.contrib import admin
from .models import Expedition, ExpeditionPhoto, ExpeditionDocument


class PhotoInline(admin.TabularInline):
    model = ExpeditionPhoto
    extra = 2


class DocumentInline(admin.TabularInline):
    model = ExpeditionDocument
    extra = 1


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'expedition_year', 'region', 'location', 'is_featured', 'is_demo_data']
    list_filter = ['region', 'is_featured', 'is_demo_data']
    search_fields = ['name', 'objectives', 'findings']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_featured', 'is_demo_data']
    inlines = [PhotoInline, DocumentInline]
