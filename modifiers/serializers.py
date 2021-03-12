import io
from mongoengine import fields
from rest_framework_mongoengine import serializers as MongoSerializer
from rest_framework import serializers
from .models import Modifiers, Options, OptionGroups, Items
from rest_framework.parsers import JSONParser


# class OptionSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#     price = serializers.FloatField()


    
class ModifierSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = Modifiers
        fields = ('id', 'name', 'options')
        depth = 2
class OptionsSerializer(MongoSerializer.DocumentSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)
    class Meta:
        model = Options
        fields = [
                "name",
                "description",
                "price",
                "modifiers",
                "type"
                ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['description']:
            data['description'] = ''
        if not data['type']:
            data['type'] = ''
        return data
    def update(self, instance, validated_data):
        print(validated_data)
        modifiers_data = validated_data.pop("modifiers")
        modifiers = instance.modifiers

class OptionGroupSerializer(MongoSerializer.DocumentSerializer):
    options = OptionsSerializer(many=True)
    class Meta:
        model = OptionGroups
        fields = '__all__'


class ItemsSerializer(MongoSerializer.DocumentSerializer):
    '''
    options = OptionsSerializer(many=True, read_only= True)
    option_groups = OptionGroupSerializer(many=True, read_only=True)
    '''
    class Meta:
        model = Items
        fields = [
                "name",
                "description",
                "type",
                "image_url",
                "price",
                "active",
                "stock",
                "option_groups",
                "options"
                ]
        depth = 3


class StoresSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = OptionGroups
        fields = '__all__'


class OrdersSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = OptionGroups
        fields = '__all__'
