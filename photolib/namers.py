import os

from django.conf import settings
from imagekit.utils import suggest_extension


def size_aware(generator):

    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        dirname = settings.IMAGEKIT_CACHEFILE_DIR
    else:
        path = os.path.splitext(source_filename)[0]
        dirname = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR, path)

    hashy = generator.get_hash()

    for processor in generator.processors:
        if hasattr(processor, 'width') and hasattr(processor, 'height'):
            if processor.width == processor.height:
                hashy = '%dsq' % processor.width
            else:
                hashy = '%d' % processor.width

    ext = suggest_extension(source_filename or '', generator.format)
    return os.path.normpath('%s-%s%s' % (dirname, hashy, ext))
