from mongoengine import *

from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, ImageField, IntField, ListField, StringField, \
    ReferenceField
# from django.db import models
# from django.contrib.postgres.fields import JSONField
#
# from rest_framework import serializers, viewsets, response


class ModOptions(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    price = FloatField(required=True)


class Hotel(models.Model):
    name = models.CharField(max_length=50)
    hotel_Main_Img = models.ImageField(upload_to='images/')


class Modifiers(Document):
    name = StringField(max_length=1024, required=True)
    options = ListField(EmbeddedDocumentField(ModOptions))


class Options(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    price = FloatField(required=True)
    modifiers = ListField(ReferenceField('Modifiers'))


class OptionGroups(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    default_order = IntField()
    min_required = IntField()
    price_default = FloatField()
    max_allowed = IntField()
    options = ListField(ReferenceField(Options))


class Items(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    type = StringField(max_length=1000)
    image_url = StringField(max_length=1000) # File to e sent
    price = FloatField()
    active = IntField()
    stock = IntField()
    option_groups = ListField(ReferenceField(OptionGroups))
    options = ListField(ReferenceField(Options))
    max_allowed = IntField()
    min_required = IntField()
    price_default = FloatField()
    display_order = IntField()


class Address(EmbeddedDocument):
    address1 = StringField(max_length=100, required=True)
    apt_bldg = StringField(max_length=1000)
    city = StringField(max_length=1000)
    state = StringField(max_length=1000)
    zip = StringField(max_length=1000)


class Timings(EmbeddedDocument):
    open = StringField(max_length=1000)
    close = StringField(max_length=1000)


class Days(EmbeddedDocument):
    Monday = ListField(EmbeddedDocumentField(Timings))
    Tuesday = ListField(EmbeddedDocumentField(Timings))
    Wednesday = ListField(EmbeddedDocumentField(Timings))
    Thursday = ListField(EmbeddedDocumentField(Timings))
    Friday = ListField(EmbeddedDocumentField(Timings))
    Saturday = ListField(EmbeddedDocumentField(Timings))
    Sunday = ListField(EmbeddedDocumentField(Timings))


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
    special_hours = ListField(EmbeddedDocumentField(SpecialHours))


class Phone(EmbeddedDocument):
    cell = StringField(max_length=1000)
    other = StringField(max_length=1000)


class Customer(Document):
    full_name = StringField(max_length=1000)
    short_name = StringField(max_length=1000)
    address = ListField(EmbeddedDocumentField(Address))
    phone = ListField(EmbeddedDocumentField(Phone))
    email = StringField(max_length=1000)


class OrderItems(EmbeddedDocument):
    name = StringField(max_length=1000)
    size = StringField(max_length=1000)
    quantity = IntField()
    price = IntField()
    side = StringField(max_length=1000)


class Orders(Document):
    number = StringField(max_length=1000)
    date = StringField(max_length=1000)
    customer = ListField(ReferenceField(Customer))
    type = StringField(max_length=1000)
    total_items = IntField()
    payment = StringField(max_length=1000)
    payment_type = StringField(max_length=1000)
    sub_total = IntField()
    tax = IntField()
    discount = IntField()
    total_price = IntField()
    items = ListField(EmbeddedDocumentField(OrderItems))




