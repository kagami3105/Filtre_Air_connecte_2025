from django.contrib import admin

from .models import Filter, MicrocontrollerData

@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'status', 'fan_speed', 'last_maintenance') 
    search_fields = ('name', 'location')

@admin.register(MicrocontrollerData)
class MicrocontrollerDataAdmin(admin.ModelAdmin):
    list_display = ('filter', 'temperature', 'humidity', 'timestamp')
    list_filter = ('filter',)
