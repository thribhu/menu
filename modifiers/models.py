from mongoengine import * 

from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField, FloatField, ImageField, IntField, ListField, StringField, ReferenceField

class ModOptions(EmbeddedDocument):
    name = StringField(max_length=100, required=True)
    price = FloatField(required=True)
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