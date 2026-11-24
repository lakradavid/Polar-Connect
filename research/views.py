from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ResearchPublication


def research_list(request):
    qs = ResearchPublication.objects.filter(status='approved')
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    year = request.GET.get('year', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(authors__icontains=q) | Q(abstract__icontains=q) | Q(keywords__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if year:
        qs = qs.filter(publication_year=year)
    return render(request, 'research/list.html', {
        'papers': qs, 'q': q, 'category': category, 'year': year,
        'categories': ResearchPublication.CATEGORY_CHOICES,
    })


def research_detail(request, pk):
    paper = get_object_or_404(ResearchPublication, pk=pk)
    if paper.status != 'approved' and not (request.user.is_authenticated and
       (request.user.is_admin_role or paper.uploaded_by == request.user)):
        messages.error(request, 'This paper is not yet publicly available.')
        return redirect('research:list')
    paper.view_count += 1
    paper.save(update_fields=['view_count'])
    related = ResearchPublication.objects.filter(category=paper.category, status='approved').exclude(pk=pk)[:4]
    return render(request, 'research/detail.html', {'paper': paper, 'related': related})


@login_required
def research_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('research:upload')
        paper = ResearchPublication(
            title=title,
            authors=request.POST.get('authors', ''),
            institution=request.POST.get('institution', ''),
            abstract=request.POST.get('abstract', ''),
            keywords=request.POST.get('keywords', ''),
            category=request.POST.get('category', 'antarctic'),
            journal_name=request.POST.get('journal_name', ''),
            doi=request.POST.get('doi', ''),
            external_link=request.POST.get('external_link', ''),
            uploaded_by=request.user,
            status='approved' if request.user.is_admin_role else 'pending',
        )
        year = request.POST.get('publication_year', '')
        if year:
            try:
                paper.publication_year = int(year)
            except ValueError:
                pass
        if request.FILES.get('paper_file'):
            paper.paper_file = request.FILES['paper_file']
        if request.FILES.get('cover_image'):
            paper.cover_image = request.FILES['cover_image']
        paper.save()
        messages.success(request, 'Research paper submitted successfully. It will be reviewed before public display.')
        return redirect('research:detail', pk=paper.pk)
    return render(request, 'research/upload.html', {'categories': ResearchPublication.CATEGORY_CHOICES})


@login_required
def approve_paper(request, pk):
    if not request.user.is_admin_role:
        messages.error(request, 'Permission denied.')
        return redirect('research:list')
    paper = get_object_or_404(ResearchPublication, pk=pk)
    action = request.POST.get('action', 'approve')
    paper.status = 'approved' if action == 'approve' else 'rejected'
    paper.save(update_fields=['status'])
    messages.success(request, f'Paper {paper.status}.')
    return redirect('dashboard:admin')
