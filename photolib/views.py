import json
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from taggit.models import Tag

from photolib.forms import PhotoUpdateForm
from photolib.models import Photo

PHOTOS_PER_PAGE = getattr(settings, 'PHOTOS_PER_PAGE', 20)


class ImageDetailView(DetailView):
    model = Photo
    queryset = Photo.objects.visible()
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


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