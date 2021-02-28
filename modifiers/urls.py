from .views import ModifierViewSet, OptionsViewSet, OptionGroupViewSet
from django.urls import path, include
from rest_framework_mongoengine.routers import DefaultRouter
router = DefaultRouter()
router.register(r'modifiers', ModifierViewSet, basename="modifiers")
router.register(r'options', OptionsViewSet, basename="options")
router.register(r'groups', OptionGroupViewSet, basename="option_groups")
urlpatterns = [
    path('', include(router.urls))
]
