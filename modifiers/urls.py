from .views import ModifierViewSet, OptionsViewSet, OptionGroupViewSet, ItemsViewSet, StoresViewSet, OrdersViewSet
from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
router = DefaultRouter()
router.register(r'modifiers', ModifierViewSet, basename="modifiers")
router.register(r'options', OptionsViewSet, basename="options")
router.register(r'groups', OptionGroupViewSet, basename="option_groups")
router.register(r'items', ItemsViewSet, basename="items")
router.register(r'stores', StoresViewSet, basename="stores")
router.register(r'orders', OrdersViewSet, basename="orders")
urlpatterns = [
    path('', include(router.urls))
]

