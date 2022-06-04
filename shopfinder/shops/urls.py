from django.urls import path
from . import views

urlpatterns = [
    path('city/',views.list_city,name='list-city'),
    path('<int:city_id>/street/',views.list_streets,name='list-streets'),
    path('shop/',views.shopfinder_view,name='shopfinder')
]