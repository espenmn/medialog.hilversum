# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from medialog.hilversum import _

class IProloog(model.Schema):
    """ Marker interface for proloog
    """
    model.load("proloog.xml")

@implementer(IProloog)
class Proloog(Item):
    """ Content-type class for Proloog
    """