from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'
        unique_together = ('name', 'region')

    def __str__(self):
        return self.name


class Employer(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    logo = models.ImageField()
    site = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)

    class Meta:
        verbose_name = 'работодатель'
        verbose_name_plural = 'работодатели'
        unique_together = (('name', 'city'), ('short_name', 'city'))

    def __str__(self):
        return self.name
