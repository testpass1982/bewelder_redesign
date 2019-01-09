from django.db import models
# from ckeditor_uploader.fields import RichTextUploadingField
# from django.utils import timezone

# Create your models here.

class Category(models.Model):
    """category model class"""
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

# class ContentMixin(models.Model):
#     """base class for vacancy and resume"""
#     title = models.CharField(u"Название", max_length=80)
#     short_description = models.CharField(
#         u'Краткое описание', max_length=200, blank=True)
#     description =RichTextUploadingField(verbose_name='Текст')
#     category = models.ForeignKey(
#         Category, verbose_name='Категория', on_delete=models.CASCADE, blank=True)
#     created_date = models.DateTimeField(u'Дата создания', default=timezone.now)
    
#     class Meta:
#         abstract = True

# class Vacancy(ContentMixin):
#     """child of contentmixin to make vacancy"""
#     published = models.BooleanField(
#         verbose_name='Опубликовать в ленте вакансий', default=False)

#     class Meta:
#         ordering = ['created_date']
#         verbose_name = 'Вакансия'
#         verbose_name_plural = 'Вакансии'
    
#     def __str__(self):
#         return self.title

# class Resume(ContentMixin):
#     """child of contentmixin to make resume"""
#     published = models.BooleanField(
#         verbose_name='Опубликовать в ленте резюме', default=False)

#     class Meta:
#         ordering = ['created_date']
#         verbose_name = 'Резюме'
#         verbose_name_plural = 'Резюме'

#     def __str__(self):
#         return self.title

