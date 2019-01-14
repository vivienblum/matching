from rest_framework.serializers import ModelSerializer
from django.conf import settings
from .models import Collection, Item

import numpy as np
import urllib
import cv2
import pdb

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

def get_average_color(url):
    # TEST
    url = settings.MEDIA_ROOT + '/item_image/flam.jpg'
    image = _grab_image(url=url)
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    print(avg_color)

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name')

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'image', 'collection')

    def create(self, validated_data):
        item = Item(**validated_data)

        # TODO calculate color
        # item.name = validated_data['image']
        # request
        item.save()
        get_average_color(item.image)
        return item
