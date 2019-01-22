from django.contrib.auth import get_user_model
from django.db import models


class Resume(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return 'Резюме: {} {}'.format(self.position.lower(), self.user.get_full_name())
