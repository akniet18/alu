from django.db import models

class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Location(models.Model):
    # name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=512)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def full_address(self):
        return '{}, {}, {}, {}'.format(self.city.region.country.name, self.city.region.name, self.city.name, self.address)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.city.region.country.name, self.city.region.name, self.city.name, self.address)