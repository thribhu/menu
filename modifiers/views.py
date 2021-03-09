from django.http import JsonResponse, request
from rest_framework import status, permissions, generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet
from .serializers import ModifierSerializer, OptionsSerializer, OptionGroupSerializer, OrdersSerializer, StoresSerializer, \
    ItemsSerializer
from .models import Modifiers, Options, OptionGroups, Items, Stores, Orders
from rest_framework.decorators import api_view


class ModifierViewSet(ModelViewSet):
    serializer_class = ModifierSerializer

    def get_queryset(self):
        return Modifiers.objects.all()

    def get(self, pk):
        modifier = Modifiers.objects.get(pk=pk)
        modifier_serializer = ModifierSerializer(modifier)
        return JsonResponse(modifier_serializer.data)

    def post(self, update_data):
        modifier_data = JSONParser().parse(request)
        modifier_serializer = ModifierSerializer(data=modifier_data)
        if modifier_serializer.is_valid():
            modifier_serializer.save()
            return JsonResponse(modifier_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(modifier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        modifier_update = Modifiers.objects.get(pk=update_data)
        modifier_data = JSONParser().parse(request)
        print(modifier_data)
        modifier_serializer = ModifierSerializer(modifier_update, data=modifier_data)
        if modifier_serializer.is_valid():
            modifier_serializer.save()
            return JsonResponse(modifier_serializer.data)
        return JsonResponse(modifier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, update_data):
        modifier = Modifiers.objects.get(pk=update_data)
        modifier.delete()
        return JsonResponse({'message': 'Modifier was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class OptionsViewSet(ModelViewSet):
    serializer_class = OptionsSerializer

    def get_queryset(self):
        option_data = Options.objects.all()
        for i in option_data:
            name_list = []
            if i['modifiers']:
                for j in i['modifiers']:
                    modifier = Modifiers.objects.get(pk=j['id'])
                    modifier_serializer = ModifierSerializer(modifier)
                    y = modifier_serializer.data
                    name_list.append(y['name'])
                i['modifiers'] = name_list
        return option_data

    def get(self, pk):
        option = Options.objects.get(pk=pk)
        option_serializer = OptionsSerializer(option)
        return JsonResponse(option_serializer.data)

    def post(self, update_data):
        option_data = JSONParser().parse(request)
        option_serializer = OptionsSerializer(data=option_data)
        if option_serializer.is_valid():
            option_serializer.save()
            return JsonResponse(option_serializer.validated_data, status=status.HTTP_201_CREATED)
        return JsonResponse(option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, update_data):
        # do things...
        print('hi')
        option_update = Options.objects.get(pk=update_data)
        option_data = JSONParser().parse(request)
        option_serializer = OptionsSerializer(option_update, data=option_data)
        if option_serializer.is_valid():
            option_serializer.save()
            return JsonResponse(option_serializer.data)
        return JsonResponse(option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, update_data):
        option = Options.objects.get(pk=update_data)
        option.delete()
        return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class OptionGroupViewSet(ModelViewSet):
    # queryset = OptionGroups.objects.all()
    serializer_class = OptionGroupSerializer

    def get_queryset(self):
        group_data = OptionGroups.objects.all()
        for i in group_data:
            name_list = []
            if i['options']:
                for j in i['options']:
                    option = Options.objects.get(pk=j['id'])
                    option_serializer = OptionsSerializer(option)
                    y = option_serializer.data
                    name_list.append(y['name'])
                i['options'] = name_list
        return group_data

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

    def delete(self, update_data):
        group = OptionGroups.objects.get(pk=update_data)
        group.delete()
        return JsonResponse({'message': 'Group was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer

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



