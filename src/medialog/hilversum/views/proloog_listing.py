# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProloogListing(Interface):
    """ Marker Interface for IProloogListing"""


class ProloogListing(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('proloog_listing.pt')
    # b_size  = 100
    

    def __call__(self):
        # Implement your own actions:
        return super(ProloogListing, self).__call__()
