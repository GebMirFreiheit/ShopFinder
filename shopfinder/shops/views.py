from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from .models import City,Street,Shop

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

# def shopfinder_view(request):
#     if request.method=='POST':
#         #create new shop
#     else:
#         #list shops
