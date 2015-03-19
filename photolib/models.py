import datetime
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from taggit.managers import TaggableManager

PHOTO_SOURCES = settings.PHOTO_SOURCES
PHOTO_QUALITY = int(getattr(settings, 'PHOTO_QUALITY', 95))


def upload_path(instance, filename):
    (name, ext) = instance.filename.rsplit('.', 1)
    uuid_path = "%s/%s/%s" % (instance.uuid[:2], instance.uuid[2:4], instance.uuid[4:])
    return u'photos/%s/%s.%s' % (uuid_path, name, ext)


class SizeSpec(ImageSpec):
    format = 'JPEG'
    options = {'quality': PHOTO_QUALITY}


class Size(models.Model):

    FILL_METHOD = 1
    FIT_METHOD = 2

    METHOD_CHOICES = (
        (FILL_METHOD, 'fill'),
        (FIT_METHOD, 'fit'),
    )

    name = models.CharField(max_length=128)
    slug = models.SlugField()
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    method = models.PositiveIntegerField(choices=METHOD_CHOICES, default=FILL_METHOD)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def spec(self):
        s =


class PhotoManager(models.Manager):
    def visible(self):
        return Photo.objects.filter(deleted=False)


class Photo(models.Model):

    objects = PhotoManager()

    photo_tags = TaggableManager(blank=True, related_name='photos')

    uuid = models.CharField(max_length=32, blank=True)
    filename = models.CharField(max_length=128,
        help_text='A descriptive file name')
    alt = models.CharField(max_length=255, blank=True,
        help_text='alt attribute text for accessibility')
    caption = models.TextField(blank=True,
        help_text='Recommended text to be used as photo caption.')
    notes = models.TextField(blank=True,
        help_text='Any other notable information about this photo.')

    credits = models.TextField(blank=True,
        help_text='Credits and copyright/left.')
    source = models.CharField(max_length=32, blank=True, choices=PHOTO_SOURCES)
    source_url = models.URLField(blank=True,
        help_text='Important when citation requires link to source.')

    # image = models.ImageField(upload_to=upload_path())
    image = models.ImageField(upload_to=upload_path)
    image_1024 = ImageSpecField(source='image',
                                processors=[ResizeToFit(1024, 3600, upscale=False)],
                                options={'quality': PHOTO_QUALITY})
    image_800 = ImageSpecField(source='image',
                                processors=[ResizeToFit(800, 3600, upscale=False)],
                                options={'quality': PHOTO_QUALITY})
    image_300 = ImageSpecField(source='image',
                                processors=[ResizeToFit(300, 3600, upscale=False)],
                                options={'quality': PHOTO_QUALITY})
    image_800sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(800, 800)],
                                options={'quality': PHOTO_QUALITY})
    image_300sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(300, 300)],
                                options={'quality': PHOTO_QUALITY})
    image_180sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(180, 180)],
                                options={'quality': PHOTO_QUALITY})
    image_thumbnail = ImageSpecField(source='image',
                                processors=[ResizeToFill(200, 200)],
                                options={'quality': PHOTO_QUALITY})

    splash_600 = ImageSpecField(source='image',
                                processors=[ResizeToFill(600, 253)],
                                options={'quality': PHOTO_QUALITY})

    uploaded = models.DateTimeField(default=datetime.datetime.utcnow)
    last_updated = models.DateTimeField(blank=True, default=datetime.datetime.utcnow)

    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-uploaded',)

    def __unicode__(self):
        return u"%s/%s" % (self.uuid, self.filename)

    def get_absolute_url(self):
        return reverse('photolib.image_detail', args=[self.uuid])

    def save(self, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex[:16]
        self.last_updated = datetime.datetime.utcnow()
        super(Photo, self).save(**kwargs)

    def tags(self):
        return self.photo_tags.order_by('name')

    def tags_str(self):
        return ", ".join(t.name for t in self.tags())
