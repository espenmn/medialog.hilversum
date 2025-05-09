# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProvidersView(Interface):
    """ Marker Interface for IProvidersView"""


class ProvidersView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('providers_view.pt')

    def __call__(self):
        # Implement your own actions:
        return super(ProvidersView, self).__call__()
