from rest_framework import serializers

from .models import City,Street,Shop

class ShopSerializer(serializers.serializer):
    title = serializers.CharField(max_length=100)
    city_name = serializers.CharField(max_length=25)
    street_name = serializers.CharField(max_length=132)
    building = serializers.CharField(max_length=10)
    shopping_hours_start = serializers.TimeField(auto_now=False, auto_now_add=False)
    shopping_hours_end = serializers.TimeField(auto_now=False, auto_now_add=False)

    def create(self, validated_data: dict):
        city = City.objects.filter(title=validated_data['city_name']).first()
        if not city:
            raise serializers.ValidationError({'city':'Please enter a valid city'})
        street = Street.objects.filter(city=city,title=validated_data['street_name'])
        if not street:
            raise serializers.ValidationError({'street': 'Please enter a valid street'})

        Shop.objects.create(
            title = validated_data['title'],
            city=city,
            street=street,
            building=validated_data['building'],
            shopping_hours_start=validated_data['shopping_hours_start'],
            shopping_hours_end=validated_data['shopping_hours_end']
        )
    class Meta:
        model = Shop