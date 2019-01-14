from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from images.views import CollectionViewSet, ItemViewSet, MatchViewSet

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

collections_routers = router.register('collections', CollectionViewSet)
collections_routers.register(
    'items', ItemViewSet,
    base_name='collection-items',
    parents_query_lookups=['collection'])

router.register(r'matches', MatchViewSet, base_name='matches')
