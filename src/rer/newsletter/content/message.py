# -*- coding: utf-8 -*-
from zope.interface import implements
from rer.newsletter.interfaces import IMessage
from plone.app.contenttypes.content import Document


class Message(Document):
    implements(IMessage)
