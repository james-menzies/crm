import debug_toolbar
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.routers import Route

from core.views import ClientViewSet, ProductViewSet, MembershipViewSet, OrderViewSet, \
    OrderItemViewSet
from crm.BatchRouter import BatchRouter

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'orders', OrderViewSet, basename='orders')
batch_router = BatchRouter()
batch_router.register(r'orders/(?P<id>\d+)/items', OrderItemViewSet, basename='order-items')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(batch_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include(debug_toolbar.urls))
]
