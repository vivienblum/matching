from rest_framework.routers import DefaultRouter
from shelf.views import CollectionViewSet, ItemViewSet


router = DefaultRouter()

router.register('collections', CollectionViewSet)
router.register('items', ItemViewSet)
