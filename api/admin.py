from django.contrib import admin

from api.models import Image


@admin.register(Image)
class UserSettings(admin.ModelAdmin):
    list_display = ('name', 'upload_dt', 'resolution', 'size')
    search_fields = ('name', 'upload_dt', 'resolution', 'size')
