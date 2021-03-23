from django.http import JsonResponse, request
from django.shortcuts import get_object_or_404
from mongoengine import errors
from rest_framework import status, permissions, generics
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import  ModifierSerializer, OptionsSerializer, OptionGroupSerializer, OrdersSerializer, StoresSerializer, \
    ItemsSerializer
from .models import Modifiers, Options, OptionGroups, Items, Stores, Orders
from rest_framework.decorators import api_view


class ModifierViewSet(ModelViewSet):
    queryset = Modifiers.objects.all()
    serializer_class = ModifierSerializer
    
class OptionsViewSet(ModelViewSet):
    serializer_class=OptionsSerializer
    def get_queryset(self):
        option_data = Options.objects.all()
        return option_data
    def create(self, request, *args, **kwargs):
        data = request.data
        modifiers = data.pop("modifiers", None)
        option = Options(**data)
        option.save()
        if modifiers is not None:
            modifiers = Modifiers.objects.filter(id__in = modifiers)
            option.modifiers = modifiers
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
        option.name = data["name"]
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
        options = Options.objects.filter(id__in = options)
        group.options = options
        serializer = OptionGroupSerializer(data = group)
        if (serializer.is_valid()):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        group = self.get_object()
        data = request.data
        options = data.pop("options", None)
        options = Options.objects.filter(id__in = options)
        group.name = data["name"] or group.name
        group.max_allowed = data["max_allowed"] or group.max_allowed
        group.min_required = data["min_required"] or group.min_required
        group.price = data["price"] or group.price
        group.order = data["order"] or group.order
        group.options = options
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
        options = data.pop('options', None)
        groups = data.pop('option_groups', None)
        item = Items(**data)
        item.save()
        print(item.id)
        if options is not None:
            options = Options.objects.filter(id__in = options)
            item.options = options
        if groups is not None:
            groups = OptionGroups.objects.filter(id__in = groups)
            item.option_groups = groups
        item.save()
        serializer = ItemsSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def update(self, request):
        item_instance = self.get_objetc()
        item = request.data
        options = item.pop('options', None)
        groups = item.pop('option_groups', None)
        item_instance.name = item["name"] or item_instance.name
        item_instance.description = item["description"] or item_instance.description
        item_instance.price = item["price"] or item_instance.price
        item_instance.active = item["active"] or item_instance.active
        item_instance.stock = item["stock"] or item_instance.stock
        if options is not None:
            options = Options.objects.filter(id__in = options)
            item_instance.options = options
        if groups is not None:
            groups = OptionGroups.objects.filter(id__in = groups)
            item_instance.option_groups = groups
        item_instance.save()
        serializer = ItemsSerializer(data = item_instance)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class StoresViewSet(ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoresSerializer

    def post(self, update_data):
        store_data = JSONParser().parse(request)
        store_serializer = StoresSerializer(data=store_data)
        if store_serializer.is_valid():
            store_serializer.save()
            return JsonResponse(store_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        store_update = Stores.objects.get(pk=update_data)
        store_data = JSONParser().parse(request)
        store_serializer = StoresSerializer(store_update, data=store_data)
        if store_serializer.is_valid():
            store_serializer.save()
            return JsonResponse(store_serializer.data)
        return JsonResponse(store_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, update_data):
        group = Stores.objects.get(pk=update_data)
        group.delete()
        return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class OrdersViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OptionGroupSerializer

    def post(self, update_data):
        order_data = JSONParser().parse(request)
        order_serializer = OrdersSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse(order_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        order_update = OptionGroups.objects.get(pk=update_data)
        order_data = JSONParser().parse(request)
        order_serializer = OrdersSerializer(order_update, data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse(order_serializer.data)
        return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, update_data):
        order = Orders.objects.get(pk=update_data)
        order.delete()
        return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)



