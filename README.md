# matching
API matching an image with a collection of images.

## DEV
- Export `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_STORAGE_BUCKET_NAME`
- Run `redis-server`
- Run `python3 manage.py runserver`
- Run `celery -A matching.celery worker -l DEBUG -E`
