import io
from mongoengine import fields
from rest_framework_mongoengine import serializers as MongoSerializer
from rest_framework import serializers 
from .models import Modifiers, Options, OptionGroups
from rest_framework.parsers import JSONParser
class OptionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    price = serializers.FloatField()
class ModifierSerializer(MongoSerializer.DocumentSerializer):
    class Meta: 
        model = Modifiers
        fields = ('id', 'name', 'options')
class OptionsSerializer(MongoSerializer.DocumentSerializer):
    class Meta: 
        model = Options
        fields = '__all__'
    def create(self, validated_data):
        modifiers = validated_data.pop('modifiers')
        instance = Options.objects.create(**validated_data)
        instance.modifiers = [Options.objects.get(pk=option) for option in modifiers]
        instance.save()
        return instance
class OptionGroupSerialzer(MongoSerializer.DocumentSerializer):
    class Meta:
        model =OptionGroups
        fields = '__all__'