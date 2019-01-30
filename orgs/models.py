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
        return '{city} ({region})'.format(city=self.name, region=self.region.name)


class EmployerManager(models.Manager):
    def create(self, *args, **kwargs):
        """
        Check arguments and if 'short_name' is not defined create it.
        """
        if 'name' not in kwargs:
            raise Exception('Employer\'s argument "name" is not defined')
        if ('short_name' not in kwargs) or (kwargs['short_name'] == ''):
            kwargs['short_name'] = kwargs['name']

        return super(EmployerManager, self).create(*args, **kwargs)


class Employer(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    logo = models.ImageField(blank=True, null=True)
    site = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255)
    # Custom Manager
    objects = EmployerManager()

    class Meta:
        verbose_name = 'работодатель'
        verbose_name_plural = 'работодатели'
        unique_together = (('name', 'city'), ('short_name', 'city'))

    def __str__(self):
        return '{employer} ({city})'.format(employer=self.short_name, city=self.city.name)

    def get_vacancy_count(self):
        from vacancies.models import Vacancy
        return Vacancy.objects.filter(employer=self.id).count()
