from rest_framework import routers
from rest_framework.routers import Route


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
            mapping={'delete': 'delete_all'},
            name='{basename}-delete-all',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/$',
            mapping={'put': 'update_all'},
            name='{basename}-update-all',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'patch': 'partial_update'},
            name='{basename}-update-one',
            detail=True,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'delete': 'destroy'},
            name='{basename}-destroy',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        )
    ]
