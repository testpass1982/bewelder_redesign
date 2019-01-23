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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'резюме'
        verbose_name_plural = 'резюме'
        ordering = ['-created']

    def __str__(self):
        return 'Резюме: {} {}'.format(self.position.lower(), self.user.get_full_name())
    
    @property
    def salary(self):
        if self.salary_min and self.salary_max:
            return '{}-{}'.format(self.salary_min, self.salary_max)
        elif self.salary_min:
            return 'от {}'.format(self.salary_min)
        elif self.salary_max:
            return 'до {}'.format(self.salary_max)
        else:
            return ''

    @property
    def experience_str(self):
        if not self.experience:
            return '0 лет'
        mod = self.experience % 10
        if mod == 1 and self.experience != 11:
            return '{} год'.format(self.experience)
        elif 1 < mod < 5 and (self.experience < 10 or self.experience > 20):
            return '{} года'.format(self.experience)
        
        return '{} лет'.format(self.experience)
