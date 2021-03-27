from django.db import models
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import BooleanField, EmbeddedDocumentField, FloatField, IntField, ListField, StringField, \
    ReferenceField

#from modifiers.models import Modifiers

class Options(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=1000, blank=True, null=True)
    price = FloatField(required=True, min_value=0)
    modifiers = ListField(ReferenceField("Modifiers"))
    image_url = StringField(max_length=1000) 
    type = StringField(max_length=100, blank=False)
    is_used = IntField(default=0, min_value=0)
    

    def __str__(self) -> str:
        return self.name
    
