from enum import unique
from re import M
from typing import List
from django.http import request
from mongoengine import *
from mongoengine import document

from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, EmbeddedDocumentField, FloatField, ImageField, IntField, ListField, StringField, \
    ReferenceField, URLField
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
    name = StringField(max_length=1024, required=True, unique=True)
    options = ListField(EmbeddedDocumentField('ModOptions'))
    # adding meta dict will excepts the unknown field error raised by 
    # mongoengine base document
    meta = {"strict": False}
    def __str__(self) -> str:
        return self.name

    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()

class Options(Document):
    name = StringField(max_length=100, required=True, unique=True)
    description = StringField(max_length=1000, default="")
    price = FloatField(required=True)
    modifiers = ListField(ReferenceField('Modifiers', reverse_delete_rule=DENY))
    image_url = StringField() 
    type = StringField(max_length=100, default="")
    meta = {'strict': False}
    def __unicode__(self):
        return self.name
    def __str__(self) -> str:
        return self.name
    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()

class OptionGroups(Document):
    name = StringField(max_length=100, required=True, unique=True)
    description = StringField(max_length=1000, default="")
    order = IntField()
    min_required = IntField()
    price = FloatField()
    max_allowed = IntField()
    options = ListField(ReferenceField('Options', reverse_delete_rule=DENY))
    meta = {"strict": False}
    def __str__ (self):
        return self.name
    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()

class Items(Document):
    name = StringField(max_length=100, required=True, unique=True)
    description = StringField(max_length=1000, default="")
    type = StringField(max_length=1000, default="")
    image_url = StringField(max_length=1000, default="") # File to e sent
    price = FloatField()
    active = IntField()
    stock = IntField()
    option_groups = ListField(ReferenceField("OptionGroups", reverse_delete_rule=DENY))
    options = ListField(ReferenceField("Options", reverse_delete_rule=DENY))

    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()

class Address(EmbeddedDocument
):
    address1 = StringField(max_length=100, required=True) ,
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
    order_histort = ListField(ReferenceField("Orders"))

class OrderItems(Document):
    name = StringField(max_length=1000)
    price = IntField()
    qty = IntField()    
    meta = {'strict': False}

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

