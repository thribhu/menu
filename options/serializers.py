
import sys, os.path
from mongoengine import fields
from rest_framework_mongoengine import serializers as MongoSerializer
#from .models import Options
#from modifiers.serializers import ModifierSerializer 

#from modifiers.serialziers import ModifierSerializer, ItemSerializer, OptionGoupSerializer
class OptionSerializer(MongoSerializer.DocumentSerializer):
    modifiers = 'modifiers.serializers'.ModifierSerializer(many=True, read_only=True)
    class Meta:
        model = 'Options'
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['description']:
            data['description'] = ''
        if not data['type']:
            data['type'] = ''
        return data
    def update(self, instance, validated_data):
        #print(validated_data)
        return super().update(instance, validated_data)