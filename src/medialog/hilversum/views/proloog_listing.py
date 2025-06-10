# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface
from medialog.hilversum.interfaces import IProloogSettings
from plone import api
#from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProloogListing(Interface):
    """ Marker Interface for IProloogListing"""


class ProloogListing(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('proloog_listing.pt')
    b_size  = 1000            
    

    def __call__(self):
        # Implement your own actions:
        self.tablelist = self.get_tablelist()
        self.header_fields = self.get_header_fields()
        return super(ProloogListing, self).__call__()
    
    def get_tablelist(self):
        return   api.portal.get_registry_record('table_fields', interface=IProloogSettings)
        

    def get_header_fields(self):
        factory = getUtility(IVocabularyFactory, name="medialog.hilversum.ProloogKeywords")
        vocab = factory(self.context)
        filter_list = []
        for field in self.get_tablelist():
            value = vocab.getTerm(field)
            filter_list.append(value)
        return filter_list
