from django.contrib import admin
from . import models


class AdminCV(admin.ModelAdmin):
    list_display = (
        'id', 'firstname', 'lastname', 'skills',
        'bio', 'projects', 'contacts',
    )
    list_filter = ('firstname', 'lastname',)
    

class RequestLogAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'http_method', 'path', 'timestamp',
    )
    list_filter = ('http_method', 'timestamp',)

admin.site.register(models.ModelCV, AdminCV)
admin.site.register(models.RequestLog, RequestLogAdmin)