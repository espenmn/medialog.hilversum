# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProlongView(Interface):
    """ Marker Interface for IProlongView"""


class ProlongView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('prolong_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def aanbieders(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        # Get unique values from 'aanbieder' index
        index = catalog._catalog.getIndex('aanbieder')
        if hasattr(index, 'uniqueValues'):
            return  index.uniqueValues()
        else:
            return None
 
    # get keyword by calling with  index name
    def get_keyword(self, keyword):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        # Get unique values from 'aanbieder' index
        index = catalog._catalog.getIndex(keyword)
        if hasattr(index, 'uniqueValues'):
            return  index.uniqueValues()
        else:
            return None