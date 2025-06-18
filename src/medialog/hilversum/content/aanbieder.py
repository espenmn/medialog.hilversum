# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText

from medialog.hilversum import _

class IAanbieder(model.Schema):
    """ Marker interface for Aanbieder
    """
    infotext = RichText(
        title=u"Infotext",
        required=False
    )

@implementer(IAanbieder)
class Aanbieder(Item):
    """ Content-type class for Aanbieder
    """
   
 
# firstletter = schema.TextLine(
#     title=u"For the index",
#     required=False
# )

    
    