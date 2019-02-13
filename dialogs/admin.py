from django.contrib import admin

from dialogs import models

admin.site.register(models.Dialog)
admin.site.register(models.Membership)
admin.site.register(models.Message)
