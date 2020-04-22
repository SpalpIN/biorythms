from django.contrib import admin
from . import models

# Register your models here.

#admin.site.register(models.Human, AuthorAdmin)
admin.site.register(models.Human)
admin.site.register(models.BiorythmsModel)