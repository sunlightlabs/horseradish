from django.conf.urls import patterns, url
from photolib.views import ImageListView, ImageDetailView, ImageUpdateView, ImageUploadView, TaggedImageListView, TagListView

urlpatterns = patterns('',
    url(r'^image/(?P<uuid>\w+)/$', ImageDetailView.as_view(), name='photolib.image_detail'),
    url(r'^image/(?P<uuid>\w+)/edit/$', ImageUpdateView.as_view(), name='photolib.image_edit'),
    url(r'^tags/(?P<slug>[\w-]+)/$', TaggedImageListView.as_view(), name='photolib.tagged_list'),
    url(r'^tags/$', TagListView.as_view(), name='photolib.tag_list'),
    url(r'^upload/$', ImageUploadView.as_view(), name='photolib.image_upload'),
    url(r'^$', ImageListView.as_view(), name='photolib.image_list'),
)

