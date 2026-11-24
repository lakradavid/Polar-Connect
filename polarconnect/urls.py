from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.global_search, name='search'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('repository/', include('repository.urls', namespace='repository')),
    path('research/', include('research.urls', namespace='research')),
    path('education/', include('education.urls', namespace='education')),
    path('expeditions/', include('expeditions.urls', namespace='expeditions')),
    path('gallery/', include('media_gallery.urls', namespace='media_gallery')),
    path('news/', include('news.urls', namespace='news')),
    path('community/', include('community.urls', namespace='community')),
    path('stations/', include('stations.urls', namespace='stations')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
