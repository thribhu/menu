from mongoengine import *

from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, EmbeddedDocumentField, FloatField, IntField, ListField, StringField, \
    ReferenceField
# from django.db import models
# from django.contrib.postgres.fields import JSONField
#
# from rest_framework import serializers, viewsets, response


class ModOptions(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    price = FloatField(required=True)


class Modifiers(Document):
    name = StringField(max_length=1024, required=True)
    options = ListField(EmbeddedDocumentField('ModOptions'))
    is_used = BooleanField(default=False)
    is_used_counter = IntField(default=0)


class Options(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000, blank=True)
    price = FloatField(required=True)
    modifiers = ListField(ReferenceField('Modifiers'))
    type = StringField(max_length=100, blank=False)
    is_used = BooleanField(default=False)
    is_used_counter = IntField(default=0)

    def __str__(self) -> str:
        return self
    
    """
    Options Update modifiers
    Arguments: *args
        modifiers list
    Returns:
        [status]: [number]
    """
        

class OptionGroups(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000, default=None)
    default_order = IntField()
    min_required = IntField()
    price_default = FloatField()
    max_allowed = IntField()
    options = ListField(ReferenceField('Options'))
    is_used = BooleanField(default=False)
    is_used_counter = IntField(default=0)


class Items(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000)
    type = StringField(max_length=1000)
    image_url = StringField(max_length=1000) # File to e sent
    price = FloatField()
    active = IntField()
    stock = IntField()
    option_groups = ListField(ReferenceField("OptionGroups"))
    options = ListField(ReferenceField("Options"))


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




