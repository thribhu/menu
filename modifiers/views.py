from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import ModifierSerializer, OptionsSerializer, OptionGroupSerialzer
from .models import Modifiers, Options, OptionGroups

class ModifierViewSet(ModelViewSet):
    serializer_class = ModifierSerializer
    
    def get_queryset(self):
        return Modifiers.objects.all()
class OptionsViewSet(ModelViewSet):
    serializer_class = OptionsSerializer
    
    def get_queryset(self):
        return Options.objects.all()
class OptionGroupViewSet(ModelViewSet):
    queryset = OptionGroups.objects.all()
    serializer_class = OptionGroupSerialzer