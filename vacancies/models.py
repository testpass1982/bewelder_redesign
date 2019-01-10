from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mainapp.models import Category
from django.utils import timezone
# Create your models here.

class Level(models.Model):
    LEVEL_CHOICES = (
        ('I', '1 уровень'),
        ('II', '2 уровень'),
        ('III', '3 уровень'),
        ('IV', '4 уровень'),
    )
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Vacancy(models.Model):
    """base class for vacancy model"""
    title = models.CharField(u"Название", max_length=80)
    salary_min = models.IntegerField(u'Зарплата от', blank=True)
    salary_max = models.IntegerField(u'Зарплата до', blank=True)
    naks_att_level = models.ManyToManyField(Level) 
    short_description = models.CharField(
        u'Краткое описание вакансии', max_length=200, blank=True)
    description =RichTextUploadingField(verbose_name='Описание вакансии') 
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE, blank=True)
    created_date = models.DateTimeField(u'Дата создания', default=timezone.now)
    published = models.BooleanField(
        verbose_name='Опубликовать в ленте вакансий', default=False)

    class Meta:
        ordering = ['created_date']
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
    
    def __str__(self):
        return self.title