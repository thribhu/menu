import io
from mongoengine import fields
from rest_framework_mongoengine import serializers as MongoSerializer
from rest_framework import serializers
from .models import (
    Customer, Modifiers, Options, OptionGroups, Items, OrderItems, FileUpload
)
from django.core.files.storage import default_storage
from pathlib import Path
from django.conf import settings
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

    def get_mongo_file_args(self):
        uploaded_file = self.validated_data["file"]
        file_obj = uploaded_file.file
        content_type = uploaded_file.content_type
        filename = uploaded_file.name
        return {
            "file_obj": file_obj,
            "content_type": content_type,
            "filename": filename
        }

    def get_file_save_args(self):
        uploaded_file = self.validated_data["file"]
        return uploaded_file.name, uploaded_file.file

    def storage_file_store(self):
        return default_storage.save(*self.get_file_save_args())

    def storage_file_delete(self):
        if not self.instance:
            raise ValueError("'instance' attribute must not be None")
        path_str = f"{settings.MEDIA_ROOT}/{self.instance.location}"
        Path(path_str).unlink()

    def create(self, validated_data):
        instance = FileUpload()
        instance.file.put(**self.get_mongo_file_args())
        path = self.storage_file_store()
        instance.location = path
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if validated_data["file"]:  # whether the input data has a file or not
            instance.file.replace(**self.get_mongo_file_args())
            self.storage_file_delete()  # deleting existing file
            path = self.storage_file_store()  # creating new file
            instance.location = path  # saving location to DB
            instance.save()
        return instance
