from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.routers import Route

from core.views import ClientViewSet, ProductViewSet, MembershipViewSet, OrderViewSet, \
    OrderItemViewSet


class BatchRouter(routers.DefaultRouter):
    """A router that is designed for batch updates on the `OrderItem` entity."""
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'post': 'create'},
            name='{basename}-create',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}$',
            mapping={'delete': 'delete-all'},
            name='{basename}-delete-all',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/$',
            mapping={'put': 'update-all'},
            name='{basename}-update-all',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'patch': 'update-one'},
            name='{basename}-update-one',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'delete': 'delete-one'},
            name='{basename}-delete-one',
            detail=True,
            initkwargs={}
        )
    ]


router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'orders', OrderViewSet)
batch_router = BatchRouter()
# batch_router.register(r'', OrderItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('orders/<id>/items', include(batch_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
