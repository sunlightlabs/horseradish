from django.contrib import admin

from photolib.models import Photo


def tags_str(obj):
    return ", ".join(t.name for t in obj.photo_tags.order_by('name'))
tags_str.short_description = 'Tags'

def source_str(obj):
    return obj.source or ''
source_str.short_description = 'Source'


class PhotoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('uuid', 'filename', 'image', 'last_updated', 'uploaded', 'notes')
        }),
        ('Content', {
            'fields': ('alt', 'caption', 'photo_tags')
        }),
        ('Credits', {
            'fields': ('credits', 'source', 'source_url')
        }),
    )
    list_display = ('uuid', 'filename', tags_str, source_str, 'last_updated', 'deleted')
    list_filter = ('deleted', 'source')
    read_only_fields = ('uuid', 'last_updated', 'uploaded')

admin.site.register(Photo, PhotoAdmin)
