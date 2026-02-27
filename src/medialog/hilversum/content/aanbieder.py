# -*- coding: utf-8 -*-
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichText
# from zope.schema import email  
from plone.schema import Email
# from zope.component import getUtility
from plone import api

from medialog.hilversum import _

class IAanbieder(model.Schema):
    """ Marker interface for Aanbieder
    """
    infotext = RichText(
        title=u"Infotext",
        required=False
    )   
 
    address = schema.TextLine(
        title=u"Address",
        required=False
    )
    
    web = schema.URI(
        title=u"Web",
        required=False
    )
    
    e_mail = Email(            
        title=u"e-mail",
        required=False
    ) 

@implementer(IAanbieder)
class Aanbieder(Item):
    """ Content-type class for Aanbieder
    """
    
    def get_courses(self):
        return api.content.find(portal_type=['Proloog'],  aanbieder=self.Title(), fl=['discipline'] )           
        
    @property
    def get_disciplines(self):
        brains = self.get_courses()
        disciplines = []
        for brain in brains:
            if hasattr(brain, 'discipline') and brain.discipline:
                disciplines.extend(brain.discipline)
        return sorted(set(disciplines))
   
    
 

    
    