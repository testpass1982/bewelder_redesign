from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from mainapp.models import Category
from django.utils import timezone
# Create your models here.

class Vacancy(models.Model):
    """base class for vacancy model"""
    title = models.CharField(u"Название", max_length=80)
    short_description = models.CharField(
        u'Краткое описание вакансии', max_length=200, blank=True)
    """пока оставлю описание в виде поля с поддержкой форматирования"""
    description =RichTextUploadingField(verbose_name='Описание вакансии') 
    """я сам не знаю зачем нам нужна категория, добавляю ее чисто интуитивно
    в будущем ее можно будет убрать или заменить на какую-то другую связь с другими моделями"""
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