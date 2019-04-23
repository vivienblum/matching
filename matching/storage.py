from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

class StaticRootS3BotoStorage(S3BotoStorage):
    location = settings.AWS_STATIC_DIR

class MediaRootS3BotoStorage(S3BotoStorage):
    location = settings.AWS_MEDIA_DIR
