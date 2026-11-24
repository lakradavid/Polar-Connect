from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from .models import NewsArticle, NewsCategory, Event


def news_list(request):
    qs = NewsArticle.objects.filter(status='published')
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
    if category:
        qs = qs.filter(category__slug=category)
    featured = qs.filter(is_featured=True).first()
    return render(request, 'news/list.html', {
        'articles': qs, 'featured': featured,
        'q': q, 'category': category,
        'categories': NewsCategory.objects.all(),
    })


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug, status='published')
    article.view_count += 1
    article.save(update_fields=['view_count'])
    related = NewsArticle.objects.filter(status='published').exclude(pk=article.pk)[:4]
    return render(request, 'news/detail.html', {'article': article, 'related': related})


def events_list(request):
    now = timezone.now()
    upcoming = Event.objects.filter(start_datetime__gte=now).order_by('start_datetime')
    past = Event.objects.filter(start_datetime__lt=now).order_by('-start_datetime')[:8]
    return render(request, 'news/events.html', {'upcoming': upcoming, 'past': past})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'news/event_detail.html', {'event': event})


@login_required
def news_create(request):
    if not request.user.is_admin_role:
        messages.error(request, 'Permission denied.')
        return redirect('news:list')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('news:create')
        slug_base = slugify(title)
        slug = slug_base
        counter = 1
        while NewsArticle.objects.filter(slug=slug).exists():
            slug = f'{slug_base}-{counter}'
            counter += 1
        article = NewsArticle(
            title=title,
            slug=slug,
            summary=request.POST.get('summary', ''),
            content=request.POST.get('content', ''),
            author=request.user,
            status=request.POST.get('status', 'draft'),
        )
        if article.status == 'published':
            article.published_at = timezone.now()
        if request.FILES.get('featured_image'):
            article.featured_image = request.FILES['featured_image']
        cat_id = request.POST.get('category', '')
        if cat_id:
            try:
                article.category = NewsCategory.objects.get(pk=cat_id)
            except NewsCategory.DoesNotExist:
                pass
        article.save()
        messages.success(request, 'Article created successfully.')
        return redirect('news:detail', slug=article.slug)
    return render(request, 'news/create.html', {'categories': NewsCategory.objects.all()})
