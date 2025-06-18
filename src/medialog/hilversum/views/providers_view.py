# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProvidersView(Interface):
    """ Marker Interface for IProvidersView"""


class ProvidersView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('providers_view.pt')
    b_size = 999
    
    def __call__(self):
        self.firstletters = self.get_firstletters()
        self.portal_url = self.get_portal_url()
        return super(ProvidersView, self).__call__()
    
    def get_portal_url(self):
        return api.portal.get().absolute_url()

    def get_firstletters(self):
        return sorted(set(self.context.portal_catalog.uniqueValuesFor('firstletter')))
    
