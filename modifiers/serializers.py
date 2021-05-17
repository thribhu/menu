import io
from mongoengine import fields
from rest_framework_mongoengine import serializers as MongoSerializer
from rest_framework import serializers
from .models import (
    Customer, Modifiers, Options, OptionGroups, Items, OrderItems, FileUpload
)
from rest_framework.parsers import JSONParser
    
class ModifierSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = Modifiers
        fields = "__all__"
        depth = 2
class OptionsSerializer(MongoSerializer.DocumentSerializer):
    modifiers = ModifierSerializer(many=True, read_only=True)
    class Meta:
        model = Options
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['description']:
            data['description'] = ''
        if not data['type']:
            data['type'] = ''
        return data
    def update(self, instance, validated_data):
        print(validated_data)
        return super().update(instance, validated_data)
class OptionGroupSerializer(MongoSerializer.DocumentSerializer):
    options = OptionsSerializer(many=True)
    class Meta:
        model = OptionGroups
        fields = '__all__'


class ItemsSerializer(MongoSerializer.DocumentSerializer):
        options = OptionsSerializer(many=True, read_only=True)
        option_groups = OptionGroupSerializer(many=True, read_only=True)
        class Meta:
            model = Items
            fields = "__all__"
class StoresSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = OptionGroups
        fields = '__all__'
class OrdersSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = OptionGroups
        fields = '__all__'

class CustomerSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
class OrderItemsSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = OrderItems
        fields = "__all__"


class FileUploadSerializer(MongoSerializer.DocumentSerializer):
    class Meta:
        model = FileUpload
        fields = "__all__"
