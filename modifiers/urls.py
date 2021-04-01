from .views import CustomersViewSet, OrdersViewSet, ModifierViewSet, OptionsViewSet, OptionGroupViewSet, ItemsViewSet, StoresViewSet, get_list_options_groups
from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
router = DefaultRouter()
router.register(r'modifiers', ModifierViewSet, basename="modifiers")
router.register(r'options', OptionsViewSet, basename="options")
router.register(r'groups', OptionGroupViewSet, basename="option_groups")
router.register(r'items', ItemsViewSet, basename="items")
router.register(r'stores', StoresViewSet, basename="stores")
router.register(r'orders', OrdersViewSet, basename="orders")
router.register(r'customers', CustomersViewSet, basename="customers")
urlpatterns = [
    path('', include(router.urls)),
    path('list-options-groups/', get_list_options_groups)

]

