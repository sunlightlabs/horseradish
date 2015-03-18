import json
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from imagekit import ImageSpec
from imagekit.cachefiles import ImageCacheFile
from imagekit.processors import ResizeToFill, ResizeToFit
from taggit.models import Tag

from photolib.forms import PhotoUpdateForm
from photolib.models import Photo

PHOTOS_PER_PAGE = getattr(settings, 'PHOTOS_PER_PAGE', 20)
CROP_STYLES = {
    'fill': ResizeToFill,
    'fit': ResizeToFit,
}

class CropSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': 60}


# the view

class ImageDetailView(DetailView):
    model = Photo
    queryset = Photo.objects.visible()
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ImageCropView(DetailView):
    model = Photo
    queryset = Photo.objects.visible()
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):

        photo = self.get_object()

        width = int(request.GET.get('w', photo.image.width))
        height = int(request.GET.get('h', photo.image.height))
        style = request.GET.get('s', 'fill')

        proc = CROP_STYLES.get(style, ResizeToFill)

        spec = CropSpec(source=photo.image)
        spec.processors = [proc(width, height)]

        icf = ImageCacheFile(spec)
        icf.generate()

        return HttpResponseRedirect(icf.url)


class ImageListView(ListView):
    model = Photo
    queryset = Photo.objects.visible()
    paginate_by = PHOTOS_PER_PAGE


class ImageUpdateView(UpdateView):
    model = Photo
    form_class = PhotoUpdateForm
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def has_changed(self):
        return True

    def form_valid(self, form):
        # save object again because indexing of tags
        # is weird
        resp = super(ImageUpdateView, self).form_valid(form)
        self.object.save()
        return resp


class ImageUploadView(CreateView):
    model = Photo
    fields = ['image']
    template_name = 'photolib/photo_upload.html'

    def form_valid(self, form):
        image = form.cleaned_data['image']
        self.object = Photo.objects.create(filename=image.name, image=image)
        if self.request.is_ajax():
            data = {
                'url': self.object.get_absolute_url()
            }
            content = json.dumps(data)
            return HttpResponse(content, content_type='application/json')
        return HttpResponseRedirect(self.get_success_url())


class ImageDeleteView(DeleteView):
    model = Photo
    queryset = Photo.objects.visible()
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        return self.model.objects.order_by('name')


class TaggedImageListView(ListView):
    model = Photo
    queryset = Photo.objects.visible()
    paginate_by = PHOTOS_PER_PAGE

    def get_queryset(self):
        slug = self.kwargs.get('slug', '').lower()
        return self.queryset.filter(photo_tags__slug=slug)

    def get_context_data(self):
        slug = self.kwargs.get('slug', '').lower()
        context = super(TaggedImageListView, self).get_context_data()
        if slug:
            try:
                tag = Tag.objects.get(slug=slug)
                context['tag'] = tag.name
            except Tag.DoesNotExist:
                pass
        return context
