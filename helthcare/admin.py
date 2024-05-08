from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.MyUser)
admin.site.register(models.Address)
admin.site.register(models.Catgory)
admin.site.register(models.Blog)