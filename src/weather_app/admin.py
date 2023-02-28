from django.contrib import admin
from .models import Station, Weather, Statistics
from django.contrib.auth.models import User, Group
from import_export.admin import ExportActionModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Station)
class StationAdmin(ExportActionModelAdmin):
    actions = ["export_as_csv"]
    list_filter = ('modified',)
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(Weather)
class WeatherAdmin(ExportActionModelAdmin):
    actions = ["export_as_csv"]
    list_filter = ('modified',)
    list_display = ('id', 'station', 'date', 'max_temp', 'min_temp', 'precipitation', 'created', 'modified')
    search_fields = ('id', 'station__name', 'date', 'max_temp', 'min_temp', 'precipitation')


@admin.register(Statistics)
class StatisticsAdmin(ExportActionModelAdmin):
    actions = ["export_as_csv"]
    list_filter = ('modified',)
    list_display = ('id', 'station', 'year', 'avg_max_temp', 'avg_min_temp', 'total_acc_ppt', 'created', 'modified')
    search_fields = ('id', 'station__name')
