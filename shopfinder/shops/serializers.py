from rest_framework import serializers

from .models import City,Street,Shop

class ShopSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    city_name = serializers.CharField(max_length=25)
    street_name = serializers.CharField(max_length=132)
    building = serializers.CharField(max_length=10)
    start = serializers.TimeField()
    end = serializers.TimeField()

    def create(self, validated_data):
        city = City.objects.filter(title=validated_data['city_name']).first()
        if not city:
            raise serializers.ValidationError({'city':'Please enter a valid city'})
        street = Street.objects.filter(city=city,title=validated_data['street_name']).first()
        if not street:
            raise serializers.ValidationError({'street': 'Please enter a valid street'})

        shop = Shop.objects.create(
            title = validated_data['title'],
            city=city,
            street=street,
            building=validated_data['building'],
            shopping_hours_start=validated_data['start'],
            shopping_hours_end=validated_data['end']
        )
        return shop
    # class Meta:
    #     model = Shop
    #     fields = ['title','city','street','building','shopping_hours_start','shopping_hours_end']