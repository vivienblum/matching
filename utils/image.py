from django.conf import settings
import numpy as np
import urllib
import cv2
from images.models import Item

MAX_SIZE = 100

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)

	# otherwise, the image does not reside on disk
	else:
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.urlopen(url)
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

def pixelate(image):
    h = image.shape[0]
    w = image.shape[1]

    height = 0
    width = 0

    for y in range(0, h):
        if y < h -1:
            height += 0 if np.array_equal(image[y, 0], image[y+1, 0]) else 1

    for x in range(0, w):
        if x < w -1:
            width += 0 if np.array_equal(image[0, x], image[0, x+1]) else 1

    return cv2.resize(image, (width, height))

def match(image, collection, delta):
    image = pixelate(_grab_image(stream=image))

    h = image.shape[0]
    w = image.shape[1]

    if h > MAX_SIZE or w > MAX_SIZE:
        return False

    items = []
    pattern = np.zeros(shape=(h, w), dtype=int)

    for y in range(0, h):
        for x in range(0, w):
            item = Item.objects.get_item_color(image[y, x], collection, delta)
            if item != None:
                if item not in items:
                    items.append(item)
                pattern[y, x] = item.id
            else:
                pattern[y, x] = -1

    return pattern, items
