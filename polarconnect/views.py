import json
from django.shortcuts import render
from django.db.models import Q

from research.models import ResearchPublication
from repository.models import KnowledgeResource
from education.models import LearningCategory
from expeditions.models import Expedition
from media_gallery.models import MediaAsset
from news.models import NewsArticle, Event
from accounts.models import CustomUser
from stations.models import ResearchStation
from django.utils import timezone


def home(request):
    stats = {
        'research':    ResearchPublication.objects.filter(status='approved').count(),
        'resources':   KnowledgeResource.objects.filter(is_published=True).count(),
        'expeditions': Expedition.objects.count(),
        'users':       CustomUser.objects.count(),
    }

    hero_features = [
        {'icon': 'fas fa-ship',           'title': 'Polar Expeditions'},
        {'icon': 'fas fa-flask',          'title': 'Research Papers'},
        {'icon': 'fas fa-graduation-cap', 'title': 'Learning Modules'},
        {'icon': 'fas fa-images',         'title': 'Media Gallery'},
    ]

    platform_features = [
        {'icon': 'fas fa-database',       'title': 'Knowledge Repository',  'description': 'Centralised scientific documents, reports and educational resources.',    'url': '/repository/'},
        {'icon': 'fas fa-flask',          'title': 'Research Publications', 'description': 'Peer-reviewed and institutional research papers on polar science.',         'url': '/research/'},
        {'icon': 'fas fa-graduation-cap', 'title': 'Learning Centre',       'description': 'Interactive modules, quizzes and study materials for all levels.',          'url': '/education/'},
        {'icon': 'fas fa-ship',           'title': 'Polar Expeditions',     'description': 'Detailed records of Indian and international polar expeditions.',           'url': '/expeditions/'},
        {'icon': 'fas fa-images',         'title': 'Media Gallery',         'description': 'High-quality photographs and videos from polar research missions.',         'url': '/gallery/'},
        {'icon': 'fas fa-newspaper',      'title': 'News & Events',         'description': 'Latest polar science news, announcements and upcoming webinars.',           'url': '/news/'},
        {'icon': 'fas fa-map-marked-alt', 'title': 'Interactive Map',       'description': 'Explore research stations and expedition locations on an interactive map.', 'url': '/stations/map/'},
        {'icon': 'fas fa-comments',       'title': 'Community Forum',       'description': 'Discuss, ask scientists and participate in polar science outreach.',        'url': '/community/'},
    ]

    default_learning_categories = [
        {'icon': 'fas fa-globe-americas',  'name': 'Introduction to Polar Regions',  'desc': 'Basics of Arctic and Antarctic geography and climate.'},
        {'icon': 'fas fa-leaf',            'name': 'Antarctic Ecosystems',           'desc': 'Life in the southernmost continent and surrounding waters.'},
        {'icon': 'fas fa-snowflake',       'name': 'Ice Sheets & Glaciers',          'desc': 'Understanding polar ice and its role in sea level rise.'},
        {'icon': 'fas fa-temperature-low', 'name': 'Climate Change & Polar Regions', 'desc': 'How polar environments both reflect and amplify global warming.'},
    ]

    gallery_placeholders = [
        {'src': 'https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=800&q=75', 'caption': 'Antarctic Landscape (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=600&q=75', 'caption': 'Arctic Ice (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1467579424161-6bdd8ef27cfc?w=600&q=75', 'caption': 'Polar Wildlife (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=600&q=75', 'caption': 'Aurora Australis (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1551009175-15bdf9dcb580?w=600&q=75',  'caption': 'Research Station (Illustrative)'},
    ]

    stations_qs = ResearchStation.objects.all()[:20]
    map_stations = [
        {
            'name':  s.name,
            'lat':   s.latitude,
            'lng':   s.longitude,
            'desc':  s.description[:150],
            'demo':  s.is_demo_data,
            'color': '#28C7E8',
        }
        for s in stations_qs
    ]

    featured_exp = list(
        Expedition.objects.filter(is_featured=True).order_by('-expedition_year')[:4]
    )
    if not featured_exp:
        featured_exp = list(Expedition.objects.order_by('-expedition_year')[:4])

    # Apply the same fallback-image logic used on the expeditions page
    from expeditions.views import _assign_fallback
    for i, exp in enumerate(featured_exp):
        _assign_fallback(exp, i)

    featured_res = KnowledgeResource.objects.filter(is_published=True, is_featured=True).order_by('-created_at')[:6]
    if not featured_res:
        featured_res = KnowledgeResource.objects.filter(is_published=True).order_by('-created_at')[:6]

    context = {
        'stats': stats,
        'hero_features': hero_features,
        'platform_features': platform_features,
        'latest_research': ResearchPublication.objects.filter(status='approved').order_by('-created_at')[:6],
        'featured_expeditions': featured_exp,
        'learning_categories': LearningCategory.objects.all()[:8],
        'default_learning_categories': default_learning_categories,
        'gallery_items': MediaAsset.objects.order_by('-created_at')[:5],
        'gallery_placeholders': gallery_placeholders,
        'latest_news': NewsArticle.objects.filter(status='published').order_by('-published_at')[:4],
        'upcoming_events': Event.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')[:5],
        'featured_resources': featured_res,
        'map_stations_json': json.dumps(map_stations),
    }
    return render(request, 'home.html', context)


def global_search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'all')

    category_choices = [
        ('all',         'All'),
        ('research',    'Research'),
        ('resources',   'Resources'),
        ('news',        'News'),
        ('expeditions', 'Expeditions'),
        ('media',       'Media'),
    ]

    results = {
        'research':    [],
        'resources':   [],
        'news':        [],
        'expeditions': [],
        'media':       [],
    }

    if query:
        if category in ('all', 'research'):
            results['research'] = ResearchPublication.objects.filter(
                status='approved'
            ).filter(
                Q(title__icontains=query) | Q(authors__icontains=query) |
                Q(abstract__icontains=query) | Q(keywords__icontains=query)
            )[:10]

        if category in ('all', 'resources'):
            results['resources'] = KnowledgeResource.objects.filter(
                is_published=True
            ).filter(
                Q(title__icontains=query) | Q(author__icontains=query) |
                Q(abstract__icontains=query) | Q(keywords__icontains=query)
            )[:10]

        if category in ('all', 'news'):
            results['news'] = NewsArticle.objects.filter(
                status='published'
            ).filter(
                Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
            )[:10]

        if category in ('all', 'expeditions'):
            results['expeditions'] = Expedition.objects.filter(
                Q(name__icontains=query) | Q(objectives__icontains=query) | Q(findings__icontains=query)
            )[:10]

        if category in ('all', 'media'):
            results['media'] = MediaAsset.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query)
            )[:10]

    total = sum(len(list(v)) for v in results.values())

    return render(request, 'search.html', {
        'query': query,
        'category': category,
        'category_choices': category_choices,
        'results': results,
        'total': total,
    })
