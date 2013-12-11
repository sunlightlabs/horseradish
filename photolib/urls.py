from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from photolib.views import ImageListView, ImageDetailView, ImageUpdateView, ImageUploadView, TaggedImageListView, TagListView


urlpatterns = patterns('',
    url(r'^image/(?P<uuid>\w+)/$', login_required(ImageDetailView.as_view()), name='photolib.image_detail'),
    url(r'^image/(?P<uuid>\w+)/edit/$', login_required(ImageUpdateView.as_view()), name='photolib.image_edit'),
    url(r'^tags/(?P<slug>[\w-]+)/$', login_required(TaggedImageListView.as_view()), name='photolib.tagged_list'),
    url(r'^tags/$', login_required(TagListView.as_view()), name='photolib.tag_list'),
    url(r'^upload/$', login_required(ImageUploadView.as_view()), name='photolib.image_upload'),
    url(r'^$', login_required(ImageListView.as_view()), name='photolib.image_list'),
)

