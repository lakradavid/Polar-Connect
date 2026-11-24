import json
from django.shortcuts import render, get_object_or_404
from .models import ResearchStation, MapLocation


def stations_list(request):
    stations = ResearchStation.objects.all()
    return render(request, 'stations/list.html', {'stations': stations})


def polar_map(request):
    stations = ResearchStation.objects.all()
    locations = MapLocation.objects.all()
    map_data = []
    for s in stations:
        map_data.append({'name': s.name, 'lat': s.latitude, 'lng': s.longitude,
                         'desc': s.description[:200], 'demo': s.is_demo_data, 'color': '#28C7E8', 'type': 'station'})
    for loc in locations:
        map_data.append({'name': loc.name, 'lat': loc.latitude, 'lng': loc.longitude,
                         'desc': loc.description[:200], 'demo': loc.is_demo_data, 'color': '#F39C12', 'type': loc.location_type})
    return render(request, 'stations/map.html', {
        'stations': stations,
        'map_data_json': json.dumps(map_data),
    })


def station_detail(request, slug):
    station = get_object_or_404(ResearchStation, slug=slug)
    return render(request, 'stations/detail.html', {'station': station})
