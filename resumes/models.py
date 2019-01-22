from django.contrib.auth import get_user_model
from django.db import models


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='пользователь')
    position = models.CharField('Должность', max_length=255)
    salary_min = models.PositiveIntegerField('Зарплата от', null=True, blank=True)
    salary_max = models.PositiveIntegerField('Зарплата до', null=True, blank=True)
    experience = models.PositiveIntegerField('Стаж', null=True, blank=True)
    about = models.TextField('О себе', null=True, blank=True)
    city = models.CharField('Место работы (город)', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'резюме'
        verbose_name_plural = 'резюме'

    def __str__(self):
        return 'Резюме: {} {}'.format(self.position.lower(), self.user.get_full_name())
