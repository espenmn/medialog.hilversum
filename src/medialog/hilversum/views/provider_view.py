# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProviderView(Interface):
    """ Marker Interface for IProlongView"""


class ProviderView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('prolong_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def aanbieders(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        return 'list of items for the provider'