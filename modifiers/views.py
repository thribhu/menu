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
        modifiers = Modifiers.objects.filter(id__in = data["modifiers"])
        option.modifiers = modifiers
        option.name = data["name"]
        option.save()
        serializer = OptionsSerializer(option)
        return Response(serializer.data, status=status.HTTP_200_OK)
class OptionGroupViewSet(ModelViewSet):
    queryset = OptionGroups.objects.all()
    serializer_class = OptionGroupSerializer
    '''
    def create(self, request, *args, **kwargs):
        data = request.data
        options = data.pop('options')
        options = Options.objects.filter(id__in = options)
        option_serializer = OptionsSerializer(options, many=True)
        print(20*'#')
        print(option_serializer.data)
        group = OptionGroups(**data)
        group.save()
        group.options = option_serializer.data
        serializer = OptionGroupSerializer(data=group)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, id):
        name_list = []
        if group['options']:
            for i in group['options']:
                option = Options.objects.get(pk=i['id'])
                option_serializer = OptionsSerializer(option)
                y = option_serializer.data
                name_list.append(y['name'])
            group['options'] = name_list
        return group
    def post(self, update_data):
        group_data = JSONParser().parse(request)
        group_serializer = OptionGroupSerializer(data=group_data)
        if group_serializer.is_valid():
            group_serializer.save()
            return JsonResponse(group_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        group_update = OptionGroups.objects.get(pk=update_data)
        group_data = JSONParser().parse(request)
        group_serializer = OptionGroupSerializer(group_update, data=group_data)
        if group_serializer.is_valid():
            group_serializer.save()
            return JsonResponse(group_serializer.data)
        return JsonResponse(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk= None, *args, **kwargs):
        group = self.get_object()
        data = request.data 
        options = data.pop('options', None)
        group.name = data["name"]
        group.options = options
        group.save()
        serializer = OptionGroupSerializer(data = group)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    def delete(self, update_data):
        group = OptionGroups.objects.get(pk=update_data)
        group.delete()
        return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        '''

class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    def get_queryset(self):
        items = Items.objects.all()
        return items


    def post(self, update_data):
        item_data = JSONParser().parse(request)
        item_serializer = ItemsSerializer(data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        item_update = OptionGroups.objects.get(pk=update_data)
        item_data = JSONParser().parse(request)
        item_serializer = ItemsSerializer(item_update, data=item_data)
        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, update_data):
        group = Items.objects.get(pk=update_data)
        group.delete()
        return JsonResponse({'message': 'Item was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


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



