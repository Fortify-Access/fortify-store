from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.BotConfiguration)
class BotConfigurationAdmin(admin.ModelAdmin):
    list_display = ('broadcast_channel',)
