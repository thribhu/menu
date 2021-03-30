from re import M
from django.http import request
from mongoengine import *
from mongoengine import document

from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, EmbeddedDocumentField, FloatField, IntField, ListField, StringField, \
    ReferenceField
# from django.db import models
# from django.contrib.postgres.fields import JSONField
#
# from rest_framework import serializers, viewsets, response

'''
Signal: To increate the count of referenced model, signal will trigger after post_save
'''
from mongoengine import signals
class ModOptions(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    price = FloatField(required=True)


class Modifiers(Document):
    name = StringField(max_length=1024, required=True)
    options = ListField(EmbeddedDocumentField('ModOptions'))
    used = IntField(default=0)
    # adding meta dict will excepts the unknown field error raised by 
    # mongoengine base document
    meta = {"strict": False}
    def __str__(self) -> str:
        return self.name

class Options(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000, blank=True)
    price = FloatField(required=True)
    modifiers = ListField(ReferenceField('Modifiers', reverse_delete_rule=DENY))
    image_url = StringField(max_length=1000) 
    type = StringField(max_length=100, blank=False)
    used = IntField(default=0)
    meta = {'strict': False}
    def __unicode__(self):
        return self.name
    def __str__(self) -> str:
        return self.name

    @classmethod
    def post_save(cls, sender, document, created=None, **kwargs):
        if created:
            modifiers = document["modifiers"]
            for id in modifiers:
                print(id)
                _modifier = Modifiers.objects.find(id = id)
                _modifier.used = _modifier +  1
                _modifier.save()
                '''
                
    def update_modifiers(self, req_modifiers, *args,  **kwargs):
        modifiers = set(self.modifiers)
        req_modifiers = set(req_modifiers)
        #reduce the count for removed modifier
        reduce_list = list(modifiers.difference(req_modifiers))
        increase_list = list(req_modifiers.difference(modifiers)) 
        if reduce_list is not None:
            for id in reduce_list:
               modifier = Modifiers.objects.find(id=id)
               modifier.used -= 1
               modifier.save()
        
        if increase_list is not None:
            for id in increase_list:
                modifier = Modifiers.objects.find(id = id)
                modifier.used += 1
                modifier.save()
                '''

class OptionGroups(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000, default=None)
    order = IntField()
    min_required = IntField()
    price = FloatField()
    max_allowed = IntField()
    options = ListField(ReferenceField('Options', reverse_delete_rule=DENY))
    used = IntField(min_value=0)
    meta = {"strict": False}
    def __str__ (self):
        return self.name

class Items(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    type = StringField(max_length=1000)
    image_url = StringField(max_length=1000) # File to e sent
    price = FloatField()
    active = IntField()
    stock = IntField()
    option_groups = ListField(ReferenceField("OptionGroups", reverse_delete_rule=DENY))
    options = ListField(ReferenceField("Options", reverse_delete_rule=DENY))


class Address(EmbeddedDocument
):
    address1 = StringField(max_length=100, required=True)
    apt_bldg = StringField(max_length=1000)
    city = StringField(max_length=1000)
    state = StringField(max_length=100)
    zip = StringField(max_length=8)


class Timings(EmbeddedDocument):
    open = StringField(max_length=1000)
    close = StringField(max_length=1000)


class Days(EmbeddedDocument):
    Monday = EmbeddedDocumentField(Timings)
    Tuesday = EmbeddedDocumentField(Timings)
    Wednesday = EmbeddedDocumentField(Timings)
    Thursday = EmbeddedDocumentField(Timings)
    Friday = EmbeddedDocumentField(Timings)
    Saturday = EmbeddedDocumentField(Timings)
    Sunday = EmbeddedDocumentField(Timings)


class SpecialHours(EmbeddedDocument):
    open = StringField(max_length=100)
    close = StringField(max_length=100)
    date_from = StringField(max_length=100)
    date_to = StringField(max_length=100)


class Stores(Document):
    name = StringField(max_length=100, required=True)
    number = StringField(max_length=1000)
    status = StringField(max_length=1000)
    address = ListField(EmbeddedDocumentField(Address))
    store_phone = StringField(max_length=1000)
    contact = StringField(max_length=1000)
    contact_phone = StringField(max_length=1000)
    hours = ListField(EmbeddedDocumentField(Days))
    tax = IntField()
    special_hours = ListField(EmbeddedDocumentField("SpecialHours"))


class Phone(EmbeddedDocument):
    cell = StringField(max_length=12)
    other = StringField(max_length=12)


class Customer(Document):
    full_name = StringField(max_length=1000)
    short_name = StringField(max_length=1000)
    address = ListField(EmbeddedDocumentField(Address))
    phone = ListField(EmbeddedDocumentField(Phone))
    email = StringField(max_length=1000)

class OrderItems(Document):
    name = StringField(max_length=1000)
    size = StringField(max_length=1000)
    quantity = IntField()
    price = IntField()
    side = StringField(max_length=1000)
    options = ListField(ReferenceField("Options"))


class Orders(Document):
    number = StringField(max_length=1000)
    date = StringField(max_length=1000)
    customer = ListField(ReferenceField("Customer"))
    type = StringField(max_length=1000)
    total_items = IntField()
    payment = StringField(max_length=1000)
    payment_type = StringField(max_length=1000)
    sub_total = IntField()
    tax = IntField()
    discount = IntField()
    total_price = IntField()
    items = ListField(ReferenceField(OrderItems))




signals.post_save.connect(Options.post_save, sender=Options)