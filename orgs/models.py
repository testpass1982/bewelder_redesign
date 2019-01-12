from django.db import models

# Create your models here.
class Employer(models.Model):
    name = models.CharField(u'Наименование работодателя', max_length=120, unique=True)
    city = models.CharField(u'Город', max_length=120, unique=True)
    logo = models.ImageField()

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.name