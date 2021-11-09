from rest_framework import routers
from rest_framework.routers import Route


class BatchRouter(routers.SimpleRouter):
    """A router that is designed for batch updates on the `OrderItem` entity."""
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={
                'post': 'create',
                'delete': 'destroy_all',
                'put': 'update_all'
            },
            name='{basename}-list',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={}
        )
    ]
