from django.contrib import admin
from . import models


class AdminCV(admin.ModelAdmin):

    list_display = (
        'id', 'firstname', 'lastname', 'skills',
        'bio', 'projects', 'contacts',
    )
    list_filter = ('firstname', 'lastname',)


admin.site.register(models.ModelCV, AdminCV)
