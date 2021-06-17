from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from api.models import Toilet, Rating, Report, SuggestedToilet
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportMixin


class ToiletResource(resources.ModelResource):
    class Meta:
        model = Toilet


class RatingResource(resources.ModelResource):
    class Meta:
        model = Rating


class ReportResource(resources.ModelResource):
    class Meta:
        model = Rating


class SuggestedToiletResource(resources.ModelResource):
    class Meta:
        model = SuggestedToilet


def set_open(modeladmin, request, queryset):
    queryset.update(is_open=True)


set_open.short_description = "Mark selected toilets as open"


def set_closed(modeladmin, request, queryset):
    queryset.update(is_open=False)


set_closed.short_description = "Mark selected toilets as closed"


@admin.register(Toilet)
class ToiletAdmin(ImportExportMixin, OSMGeoAdmin):
    list_display = ['id', 'name', 'address', 'rating', 'lat_lng']
    resource_class = ToiletResource
    list_filter = ('data_source', 'changing_place', 'radar_available', 'radar_only', 'disabled', 'baby_change', 'unisex', 'female_only', 'male_only', 'is_open', 'is_free')
    search_fields = ('id', 'name', 'address', 'data_source')
    actions = [set_open, set_closed]
    default_lon = 0.1278
    default_lat = 51.5074
    default_zoom = 12


@admin.register(SuggestedToilet)
class SuggestedToiletAdmin(ExportActionMixin, OSMGeoAdmin):
    date_hierarchy = 'date'
    resource_class = RatingResource
    list_display = ['date', 'location', 'details']
    default_lon = 0.1278
    default_lat = 51.5074
    default_zoom = 12


@admin.register(Rating)
class RatingAdmin(ExportActionMixin, admin.ModelAdmin):
    date_hierarchy = 'date'
    resource_class = RatingResource
    list_display = ['date', 'toilet', 'rating']


@admin.register(Report)
class ReportAdmin(ExportActionMixin, admin.ModelAdmin):
    date_hierarchy = 'date'
    resource_class = ReportResource
    list_display = ['date', 'toilet', 'reason', 'other_description']


