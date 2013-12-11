from django import forms

from photolib.models import Photo


class PhotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['filename', 'alt', 'caption', 'notes', 'credits', 'source', 'source_url', 'photo_tags']
