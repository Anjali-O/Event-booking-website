from django.contrib import admin
from .models import Event


class EventAdmin(admin.ModelAdmin):
    model=Event
    list_display=['id','title','description','venue']

admin.site.register(Event,EventAdmin)
