from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import KnowledgeResource


def resource_list(request):
    qs = KnowledgeResource.objects.filter(is_published=True)
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    rtype = request.GET.get('type', '')
    year = request.GET.get('year', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(keywords__icontains=q) | Q(abstract__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if rtype:
        qs = qs.filter(resource_type=rtype)
    if year:
        qs = qs.filter(publication_date__year=year)
    return render(request, 'repository/list.html', {
        'resources': qs, 'q': q, 'category': category, 'rtype': rtype, 'year': year,
        'categories': KnowledgeResource.CATEGORY_CHOICES,
        'types': KnowledgeResource.RESOURCE_TYPES,
    })


def resource_detail(request, pk):
    resource = get_object_or_404(KnowledgeResource, pk=pk, is_published=True)
    related = KnowledgeResource.objects.filter(category=resource.category, is_published=True).exclude(pk=pk)[:4]
    return render(request, 'repository/detail.html', {'resource': resource, 'related': related})


@login_required
def resource_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('repository:upload')
        resource = KnowledgeResource(
            title=title,
            author=request.POST.get('author', ''),
            institution=request.POST.get('institution', ''),
            abstract=request.POST.get('abstract', ''),
            keywords=request.POST.get('keywords', ''),
            category=request.POST.get('category', 'antarctic'),
            resource_type=request.POST.get('resource_type', 'pdf'),
            external_url=request.POST.get('external_url', ''),
            uploaded_by=request.user,
        )
        if request.FILES.get('uploaded_file'):
            resource.uploaded_file = request.FILES['uploaded_file']
        date_str = request.POST.get('publication_date', '')
        if date_str:
            from datetime import date
            try:
                resource.publication_date = date.fromisoformat(date_str)
            except ValueError:
                pass
        resource.save()
        messages.success(request, 'Resource uploaded successfully.')
        return redirect('repository:detail', pk=resource.pk)
    return render(request, 'repository/upload.html', {
        'categories': KnowledgeResource.CATEGORY_CHOICES,
        'types': KnowledgeResource.RESOURCE_TYPES,
    })
