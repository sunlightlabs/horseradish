from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from taggit.models import Tag

from photolib.models import Photo

PHOTOS_PER_PAGE = getattr(settings, 'PHOTOS_PER_PAGE', 20)


class ImageDetailView(DetailView):
    model = Photo
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ImageListView(ListView):
    model = Photo
    paginate_by = PHOTOS_PER_PAGE


class ImageUpdateView(UpdateView):
    model = Photo
    fields = ['filename', 'alt', 'caption', 'notes', 'credits', 'source', 'source_url', 'photo_tags']
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ImageUploadView(CreateView):
    model = Photo
    fields = ['image']
    template_name = 'photolib/photo_upload.html'

    def form_valid(self, form):
        image = form.cleaned_data['image']
        self.object = Photo.objects.create(filename=image.name, image=image)
        return HttpResponseRedirect(self.get_success_url())


class TagListView(ListView):
    model = Tag

    def get_queryset(self):
        return self.model.objects.order_by('name')


class TaggedImageListView(ListView):
    model = Photo
    paginate_by = PHOTOS_PER_PAGE

    def get_queryset(self):
        slug = self.kwargs.get('slug', '').lower()
        return self.model.objects.filter(photo_tags__slug=slug)

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