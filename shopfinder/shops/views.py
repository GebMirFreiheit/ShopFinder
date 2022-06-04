from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import City,Street,Shop
from .serializers import ShopSerializer

def list_city(request):
    cities = City.objects.all()
    context={'cities':[city.title for city in cities]}
    return JsonResponse(context,json_dumps_params={'ensure_ascii': False})

def list_streets(request,city_id):
    try:
        city = City.objects.get(pk=city_id)
    except City.DoesNotExist:
        return HttpResponse(status=400,content='Нет города с таким идентификатором')
    streets = Street.objects.filter(city=city)
    context={'streets':[street.title for street in streets]}
    return JsonResponse(context,json_dumps_params={'ensure_ascii': False})

@csrf_exempt
@api_view(['GET', 'POST'])
def shopfinder_view(request):
    if request.method=='POST':
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = serializer.create(serializer.data)
            return HttpResponse(status=200,content=shop.id)
        return JsonResponse(serializer.errors, status=400)
    else:
        qs = Shop.objects.all()
        city_id = request.GET.get('city')
        street_id = request.GET.get('street')
        is_open = request.GET.get('open')
        if city_id != None:
            try:
                qs = qs.filter(city=City.objects.get(pk=int(city_id)))
            except (City.DoesNotExist,ValueError):
                return HttpResponse(status=400,content='Невалидный параметр city')
        if street_id != None:
            try:
                qs = qs.filter(street=Street.objects.get(pk=int(street_id)))
            except (Street.DoesNotExist, ValueError):
                return HttpResponse(status=400, content='Невалидный параметр street')
        if is_open != None:
            if is_open=='1':
                qs = qs.filter(Q(shopping_hours_start__lte=timezone.now().time()) & Q(shopping_hours_end__gt=timezone.now().time()))
            elif is_open=='0':
                qs = qs.filter(Q(shopping_hours_start__gt=timezone.now().time()) | Q(shopping_hours_end__lte=timezone.now().time()))
            else:
                return HttpResponse(status=400,content='Невалидный параметр open')
        res = [{'city':shop.city.title,'street':shop.street.title,'building':shop.building,'title':shop.title} for shop in qs]
        return JsonResponse(res,safe=False,json_dumps_params={'ensure_ascii': False})
