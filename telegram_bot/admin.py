from django.contrib import admin

from .models import Logger, Messages

admin.site.register(Logger)
admin.site.register(Messages)