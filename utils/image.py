from django.conf import settings
import numpy as np
import urllib
import cv2
from .format import *
from images.models import Item
# DEV
import pdb

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

	# return the image
	return image

def get_average_color(image):
    image = _grab_image(stream=image)
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    return avg_color

def pixelate(image):
    image = _grab_image(stream=image)
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


def draw_image(items, pattern):
    print items
    print pattern
    # items_indexed[0] = "toto"

    # for row in items:
	# 	if row.id >= 0:
	# 		print row.id
	# 		items_indexed[row.id] = row

    # print items_indexed
    height = 15
    width = 15
    # print pattern.shape
    h = pattern.shape[0]
    w = pattern.shape[1]
    image_out = np.zeros((height, width, 3), np.uint8)

    for y in range(0, h):
        # print 'y'
        for x in range(0, w):
            # print 'x'
            item_match = None
            for item in items:
				# print 'item'
				if item.id == pattern[y, x]:
					item_match = item

            if item_match != None:
                print item_match.image
                image_temp = _grab_image(stream=item_match.image)
                image_temp = cv2.resize(image_temp, (32, 32))

            # while items[i].id != pattern[y, x] and i < len(items) - 1 and pattern[y, x] >= 0:
            #     print items[i].id
            #     # print(i)
            #     i += 1
            #     # print items[i].id == pattern[y, x]
            # print i
            # image_temp = _grab_image(stream=items[i].image)

			# while(items[i].id == pattern[y, x]):
			# 	i += 1
    # image_out[:,0:width//2] = (255,0,0)      # (B, G, R)
    image_out[:,width//2:width] = (0,255,0)

    # cv2.imwrite('test.png', image_out)

def match(image):
    image = pixelate(image)

    h = image.shape[0]
    w = image.shape[1]

    if h > MAX_SIZE or v > MAX_SIZE:
		return false

    items = []
    pattern = np.zeros(shape=(h, w), dtype=int)

    for y in range(0, h):
        for x in range(0, w):
            # print image[y, x]
				item = Item.objects.get_item_color(image[y, x], 5)
				if item != None:
					if item not in items:
						items.append(item)
					pattern[y, x] = item.id
					# print item.id
				else:
					pattern[y, x] = -1
				# print "No item matches"

    return pattern, items
