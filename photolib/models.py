import datetime
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from taggit.managers import TaggableManager

PHOTO_SOURCES = settings.PHOTO_SOURCES
PHOTO_QUALITY = getattr(settings, 'PHOTO_QUALITY', 80)


def upload_path(width=None):
    def inner(instance, filename):
        (name, ext) = instance.filename.rsplit('.', 1)
        print uuid
        uuid_path = "%s/%s/%s" % (instance.uuid[:2], instance.uuid[2:4], instance.uuid[4:])
        print uuid_path
        if width:
            return u'photos/%s/%s-%d.%s' % (uuid_path, name, width, ext)
        return u'photos/%s/%s.%s' % (uuid_path, name, ext)
    return inner


class Photo(models.Model):

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

    image = models.ImageField(upload_to=upload_path())
    image_1024 = ImageSpecField(source='image',
                                processors=[ResizeToFit(1024, 3600, upscale=False)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_800 = ImageSpecField(source='image',
                                processors=[ResizeToFit(800, 3600, upscale=False)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_300 = ImageSpecField(source='image',
                                processors=[ResizeToFit(300, 3600, upscale=False)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_800sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_300sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(300, 300)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_180sq = ImageSpecField(source='image',
                                processors=[ResizeToFill(180, 180)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})
    image_thumbnail = ImageSpecField(source='image',
                                processors=[ResizeToFill(200, 200)],
                                format='JPEG',
                                options={'quality': PHOTO_QUALITY})

    uploaded = models.DateTimeField(default=datetime.datetime.utcnow)
    last_updated = models.DateTimeField(blank=True, default=datetime.datetime.utcnow)

    class Meta:
        pass

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
