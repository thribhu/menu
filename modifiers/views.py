from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404
from mongoengine import errors
from mongoengine.queryset.transform import update
from rest_framework import status, permissions, generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_mongoengine.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    CustomerSerializer, ModifierSerializer, OptionsSerializer, OptionGroupSerializer,
    OrdersSerializer, StoresSerializer, ItemsSerializer, FileUploadSerializer
)
from .models import (
    Customer, Modifiers, Options, OptionGroups, Items, Stores, OrderItems,
    Orders, FileUpload
)

from rest_framework.decorators import api_view


class ModifierViewSet(ModelViewSet):
    queryset = Modifiers.objects.all()
    serializer_class = ModifierSerializer
    
class OptionsViewSet(ModelViewSet):
    #parser_classes = (MultiPartParser, FormParser)
    serializer_class=OptionsSerializer
    def get_queryset(self):
        option_data = Options.objects.all()
        return option_data
    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        modifiers = data.pop("modifiers", None)
        option = Options(**data)
        option.save()
        if modifiers:
            u_modifiers = []
            for id in modifiers:
                u_modifiers.append(Modifiers.objects.get(pk=id))
            option.modifiers = u_modifiers
            option.save()
        serializer = OptionsSerializer(option)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        option = self.get_object()
        data = request.data
        modifiers = data.pop('modifiers', None)
        u_modifiers = []
        for id in modifiers:
            u_modifiers.append(Modifiers.objects.get(pk=id))
        option.modifiers = u_modifiers
        option.name = data["name"] or option.name
        option.type = data["type"] or option.type
        option.price = data["price"] or option.price
        option.description = data["description"] or option.description
        option.image_url = data["image_url"] or option.image_url
        option.save()
        serializer = OptionsSerializer(option)
        return Response(serializer.data, status=status.HTTP_200_OK)
class OptionGroupViewSet(ModelViewSet):
    serializer_class = OptionGroupSerializer
    def get_queryset(self):
        groups = OptionGroups.objects.all()
        return groups
    def create(self, request, *args, **kwargs):
        data = request.data
        options = data.pop("options", None)
        group = OptionGroups(**data)
        group.save()
        if options is not None:
           u_options = [] 
           for id in options:
               u_options.append(Options.objects.get(id=id))
               group.options = u_options
               group.save()
        serializer = OptionGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        data = request.data
        options = data.pop("options", None)
        options_list = []
        for option in options:
            options_list.append(Options.objects.get(id=option))
        group.name = data["name"] or group.name
        group.max_allowed = data["max_allowed"] or group.max_allowed
        group.min_required = data["min_required"] or group.min_required
        group.price = data["price"] or group.price
        group.order = data["order"] or group.order
        group.options = options_list
        group.save()
        serializer = OptionGroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK) 
class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    def get_queryset(self):
        items = Items.objects.all()
        return items
    def create(self, request):
        data = request.data
        print(data)
        options = data.pop('options', None)
        groups = data.pop('option_groups', None)
        item = Items(**data)
        item.save()
        if options:
            update_list = []
            for option in options:
                _option = Options.objects.get(id = option)
                update_list.append(_option)
            item.options = update_list
        if groups:
            update_list = []
            for group in groups:
                _group = OptionGroups.objects.get(id = group)
                update_list.append(_group)
            item.option_groups = update_list
        item.save()
        serializer = ItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        item_instance = self.get_object()
        item = request.data
        print(item)
        options = item.pop('options', None)
        groups = item.pop('option_groups', None)
        item_instance.name = item["name"] or item_instance.name
        item_instance.description = item["description"] or item_instance["description"]
        item_instance.price = item["price"] or item_instance["price"]
        item_instance.active = item["active"] or item_instance["active"]
        item_instance.stock = item["stock"] or item_instance["stock"]
        item_instance.image_url = item["image_url"] or item_instance["image_url"]
        item_instance.type = item["type"] or item_instance["type"]
        if options:
            update_list = []
            for option in options:
                _option = Options.objects.get(id = option)
                update_list.append(_option)
            item_instance.options = update_list
        if groups:
            update_list = []
            for group in groups:
                _group = OptionGroups.objects.get(id = group)
                update_list.append(_group)
            item_instance.option_groups = update_list
        else:
            item_instance.option_groups = list()
        item_instance.save()
        serializer = ItemsSerializer(item_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoresViewSet(ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoresSerializer

class CustomersViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OptionGroupSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = data.pop('customer', None)
        items = data.pop('items', None)
        store = data.pop('store', None)
        if not items:
            raise ValueError('Items is required')
        for item in items:
            m_item = Items.objects.get(id = item.id)
            options = item.pop('options', None)
            option_groups = item.pop('option_groups', None)
            modifiers = items.pop('modifers', None)
            item_options = []
            item_groups = []
            item_modifiers = []
            for option in options:
                op = Options.objects.get(id = option.id)
                name = op.name

#get list options and groups in single call
@api_view(["GET"])
def get_list_options_groups(request, *args, **kwargs):
    options = Options.objects.all()
    groups = OptionGroups.objects.all()
    option_serializer = OptionsSerializer(options, many=True)
    group_serializer = OptionGroupSerializer(groups, many=True)
    print(option_serializer.data)
    res = option_serializer.data
    res = res + group_serializer.data
    context = {"data": res}
    return Response(context, status=status.HTTP_200_OK)

@api_view(["POST"])
def upload_many_options(request, *args, **kwargs):
    options_list = request.data
    print(options_list)
    options = [Options(**opt) for opt in options_list]
    Options.objects.bulk_create(options)
    serializer = OptionsSerializer(options, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileUploadViewSet(ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
