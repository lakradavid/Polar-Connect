from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import MediaAsset, MediaCategory


def gallery(request):
    qs = MediaAsset.objects.all()
    q = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    mtype = request.GET.get('type', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(tags__icontains=q) | Q(description__icontains=q))
    if category_id:
        qs = qs.filter(category_id=category_id)
    if mtype:
        qs = qs.filter(media_type=mtype)
    categories = MediaCategory.objects.all()
    placeholder_images = [
        {'src': 'https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=600&q=75', 'cap': 'Antarctic Landscape (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=600&q=75', 'cap': 'Arctic Ice Formation (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1467579424161-6bdd8ef27cfc?w=600&q=75', 'cap': 'Polar Wildlife (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=600&q=75', 'cap': 'Aurora Australis (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1551009175-15bdf9dcb580?w=600&q=75', 'cap': 'Research Station (Illustrative)'},
        {'src': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&q=75', 'cap': 'Scientific Equipment (Illustrative)'},
    ]
    return render(request, 'media_gallery/gallery.html', {
        'assets': qs, 'q': q, 'category_id': category_id, 'mtype': mtype,
        'categories': categories,
        'media_types': MediaAsset.MEDIA_TYPES,
        'placeholder_images': placeholder_images,
    })


def media_detail(request, pk):
    asset = get_object_or_404(MediaAsset, pk=pk)
    asset.view_count += 1
    asset.save(update_fields=['view_count'])
    related = MediaAsset.objects.filter(category=asset.category).exclude(pk=pk)[:6]
    return render(request, 'media_gallery/detail.html', {'asset': asset, 'related': related})


@login_required
def media_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        if not title:
            messages.error(request, 'Title is required.')
            return redirect('media_gallery:upload')
        asset = MediaAsset(
            title=title,
            description=request.POST.get('description', ''),
            media_type=request.POST.get('media_type', 'image'),
            tags=request.POST.get('tags', ''),
            photographer=request.POST.get('photographer', ''),
            location=request.POST.get('location', ''),
            embed_url=request.POST.get('embed_url', ''),
            uploaded_by=request.user,
        )
        cat_id = request.POST.get('category', '')
        if cat_id:
            try:
                asset.category = MediaCategory.objects.get(pk=cat_id)
            except MediaCategory.DoesNotExist:
                pass
        if request.FILES.get('image'):
            asset.image = request.FILES['image']
        asset.save()
        messages.success(request, 'Media uploaded successfully.')
        return redirect('media_gallery:detail', pk=asset.pk)
    return render(request, 'media_gallery/upload.html', {
        'categories': MediaCategory.objects.all(),
        'media_types': MediaAsset.MEDIA_TYPES,
    })
