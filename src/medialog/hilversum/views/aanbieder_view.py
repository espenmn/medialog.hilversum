# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import getToolByName

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProviderView(Interface):
    """ Marker Interface for IAanbiederView"""


class AanbiederView(BrowserView):
    
    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    
    def courses(self):
        # return self.context.portal_catalog(portal_type=['Prolong']d)
        return self.context.portal_catalog(portal_type=['Prolong'], aanbieder=self.context.Title())
        
 