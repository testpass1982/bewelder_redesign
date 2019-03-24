from django.db import models
from django.contrib.auth import get_user_model

from vacancies.models import Vacancy


User = get_user_model()


class Dialog(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, blank=True, null=True)
    members = models.ManyToManyField(User, through='Membership')
    theme = models.CharField(max_length=200)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return 'Диалог: {}'.format(self.theme)


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    last_check = models.DateTimeField(null=True, blank=True)
    is_creator = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('user', 'dialog'),)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}: {}'.format(self.user, self.text)
