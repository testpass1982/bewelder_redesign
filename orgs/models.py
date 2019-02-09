from django.db import models


class Region(models.Model):
    name = models.CharField('Регион', max_length=255, unique=True)

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('Город', max_length=255)
    region = models.ForeignKey(Region, verbose_name='Регион', on_delete=models.PROTECT)

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
    name = models.CharField('Полное название', max_length=255)
    short_name = models.CharField('Сокращенное название', max_length=255)
    inn = models.CharField('ИНН', max_length=12)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.PROTECT)
    logo = models.ImageField('Логотип', blank=True, null=True)
    site = models.CharField('Сайт', max_length=255, blank=True)
    phone = models.CharField('Телефон', max_length=11)
    email = models.EmailField('Эл. почта', max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Custom Manager
    objects = EmployerManager()

    class Meta:
        verbose_name = 'работодатель'
        verbose_name_plural = 'работодатели'
        unique_together = (('name', 'city'), ('short_name', 'city'))
        ordering = ['-created']

    def __str__(self):
        return '{employer} ({city})'.format(employer=self.short_name, city=self.city.name)

    def get_vacancy_count(self):
        """
        Found and count number of vacations per current Employer.
        :return: Number of vacations.
        """
        from vacancies.models import Vacancy
        return Vacancy.objects.filter(employer=self.id).count()
