from haystack import indexes

from photolib.models import Photo


class PhotoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    alt = indexes.CharField(model_attr='alt', indexed=False)
    uuid = indexes.CharField(model_attr='uuid', indexed=False)
    thumbnail_url = indexes.CharField(indexed=False, model_attr='image_thumbnail__url')

    def get_model(self):
        return Photo

    def get_updated_field(self):
        return 'last_updated'

    def index_queryset(self, using=None):
        return Photo.objects.visible()
