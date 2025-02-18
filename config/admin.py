from django.contrib import admin
from . import models as config_models
from inbounds import models as inbound_models

# Register your models here.
class InboundInline(admin.TabularInline):
    model = inbound_models.Inbound
    extra = 1


@admin.register(config_models.Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('host', 'location')
    inlines = (InboundInline,)

