from django.db import models

class City(models.Model):
    title = models.CharField(max_length=25,unique=True)

    def __str__(self):
        return self.title

class Street(models.Model):
    title = models.CharField(max_length=132,unique=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    def __str__(self):
        return self.title+'('+self.city.title+')'

class Shop(models.Model):
    title = models.CharField(max_length=100)
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    street = models.ForeignKey(Street,on_delete=models.CASCADE)
    building = models.CharField(max_length=10) #учитываем, что в номере дома могут быть литеры или дробь
    shopping_hours_start = models.TimeField(auto_now=False, auto_now_add=False)
    shopping_hours_end = models.TimeField(auto_now=False, auto_now_add=False)

    @property
    def is_night(self):
        if self.shopping_hours_start<self.shopping_hours_end:
            return False
        else:
            return True

    @property
    def is_all_day(self):
        if self.shopping_hours_start==self.shopping_hours_end:
            return True
        else:
            return False

    class Meta:
        unique_together = ['street','building','title'] #ограничение, чтобы исключить дублирование магазина в базе

