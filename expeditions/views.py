from django.shortcuts import render, get_object_or_404
from .models import Expedition

# ---------------------------------------------------------------------------
# Specific images for named expeditions — override generic fallbacks
# ---------------------------------------------------------------------------
SPECIFIC_IMAGES = {
    # 43rd Indian Scientific Expedition to Antarctica (2024) — DDNews official photo
    '43rd-indian-scientific-expedition-antarctica':
        'https://ddnews.gov.in/wp-content/uploads/2024/03/Polar.png',

    # 32nd Indian Scientific Expedition — Wikimedia Commons photo (Bharati commissioning)
    '32nd-indian-scientific-expedition-bharati':
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/'
        'Thamban_Meloth_as_part_of_the_first_Indian_Scientific_Expedition_to_South_Pole.jpg/'
        '330px-Thamban_Meloth_as_part_of_the_first_Indian_Scientific_Expedition_to_South_Pole.jpg',
}

# Generic fallback pools — used when no specific image is defined
ANTARCTIC_IMAGES = [
    'https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=700&q=80',  # Antarctic landscape
    'https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=700&q=80',  # Aurora / polar sky
    'https://images.unsplash.com/photo-1467579424161-6bdd8ef27cfc?w=700&q=80',  # Penguin colony
    'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=700&q=80',  # Arctic ice
    'https://images.unsplash.com/photo-1551009175-15bdf9dcb580?w=700&q=80',     # Research station
    'https://images.unsplash.com/photo-1519832979-6fa011b87667?w=700&q=80',     # Ocean research vessel
    'https://images.unsplash.com/photo-1504457047772-27faf1c00561?w=700&q=80',  # Science lab
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=700&q=80',  # Scientist / equipment
]

ARCTIC_IMAGES = [
    'https://images.unsplash.com/photo-1534447677768-be436bb09401?w=700&q=80',  # Arctic landscape
    'https://images.unsplash.com/photo-1508193638397-1c4234db14d8?w=700&q=80',  # Arctic ice
    'https://images.unsplash.com/photo-1476610182048-b716b8518aae?w=700&q=80',  # Aurora borealis
    'https://images.unsplash.com/photo-1517783999520-f068d7431a60?w=700&q=80',  # Snow landscape
]


def _assign_fallback(exp, index=0):
    """Attach a fallback_image attribute to an expedition object."""
    if exp.cover_image:
        exp.fallback_image = None
        return

    # 1. Check slug-specific overrides first
    if exp.slug in SPECIFIC_IMAGES:
        exp.fallback_image = SPECIFIC_IMAGES[exp.slug]
        return

    # 2. Generic pool based on region
    if exp.region == 'arctic':
        exp.fallback_image = ARCTIC_IMAGES[index % len(ARCTIC_IMAGES)]
    else:
        exp.fallback_image = ANTARCTIC_IMAGES[index % len(ANTARCTIC_IMAGES)]


def expedition_list(request):
    region = request.GET.get('region', '')
    qs = list(Expedition.objects.all())
    if region:
        qs = [e for e in qs if e.region == region]

    for i, exp in enumerate(qs):
        _assign_fallback(exp, i)

    return render(request, 'expeditions/list.html', {
        'expeditions': qs,
        'region': region,
        'region_choices': Expedition.REGION_CHOICES,
    })


def expedition_detail(request, slug):
    expedition = get_object_or_404(Expedition, slug=slug)
    _assign_fallback(expedition, 0)
    return render(request, 'expeditions/detail.html', {'expedition': expedition})
