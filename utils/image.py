from django.conf import settings
import numpy as np
import urllib
import urllib.request
import cv2
from images.models import Item, Match, Collection
from celery import shared_task
import codecs, json
from django.core import serializers

MAX_SIZE = 100000

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)

	# otherwise, the image does not reside on disk
	else:
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.request.urlopen(url)
			data = resp.read()

		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()

		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	return image

def get_average_color(image):
    image = _grab_image(stream=image)
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    return avg_color

def pixelate(match):
    image = _grab_image(url=match.image.url)
    h = image.shape[0]
    w = image.shape[1]

    maxHeight = 0
    maxWidth = 0

    for y in range(0, h):
        tmpWidth = 1
        for x in range(0, w):
            if x < w -1:
                tmpWidth += 0 if np.array_equal(image[y, x], image[y, x+1]) else 1
        if tmpWidth >= maxWidth:
            maxWidth = tmpWidth

    for x in range(0, w):
        tmpHeight = 1
        for y in range(0, h):
            if y < h -1:
                tmpHeight += 0 if np.array_equal(image[y, x], image[y+1, x]) else 1
        if tmpHeight >= maxHeight:
            maxHeight = tmpHeight
    match.nb_rows = maxHeight
    match.save()
    return cv2.resize(image, (maxWidth, maxHeight))

@shared_task
def match_images(id):
    match = Match.objects.get(pk=id)
    image = pixelate(match)
    collection = match.collection
    delta = match.collection.delta

    h = image.shape[0]
    w = image.shape[1]

    if h * w > MAX_SIZE:
        return False

    items = []
    pattern = np.zeros(shape=(h, w), dtype=int)

    for y in range(0, h):
        match.rows_done = match.rows_done+1
        match.save()
        for x in range(0, w):
            item = Item.objects.get_item_color(image[y, x], collection, delta)
            if item != None:
                if item not in items:
                    items.append(item)
                else:
                    item_to_inc_quantity = next((el for el in items if el.id == item.id), None)
                    item_to_inc_quantity.quantity = item_to_inc_quantity.quantity+1
                pattern[y, x] = item.id
            else:
                pattern[y, x] = -1

    # return pattern, items
    pattern_response = np.array(pattern).tolist()
    match.pattern = json.dumps({"data": pattern_response})
    items_response = [item.as_json() for item in items]
    match.items = json.dumps(items_response)
    match.finished = True
    match.save()
    return True
