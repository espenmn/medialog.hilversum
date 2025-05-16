# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer
from zope import schema

from medialog.hilversum import _

class IAanbieder(model.Schema):
    """ Marker interface for Aanbieder
    """

@implementer(IAanbieder)
class Aanbieder(Item):
    """ Content-type class for Aanbieder
    """