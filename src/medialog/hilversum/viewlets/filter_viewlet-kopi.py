# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
#from medialog.hilversum.keywords import get_keywords as keywords
from medialog.hilversum.keywords import get_discipline as discipline
from medialog.hilversum.interfaces import IProloogSettings
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
#from urllib.parse import unquote


class FilterViewlet(ViewletBase):
            
    def index(self):
        return super(FilterViewlet, self).render()

    def update(self):
        self.keyword = self.get_keyword()
        self.filters = self.get_filters()
        self.site_url = self.site_url()
        
    def site_url(self):
        return api.portal.get().absolute_url()
        
    # get keyword by calling with  index name
    def get_discipline(self):
        return discipline(self)

    # # get keyword by calling with all index name, as loop
    def get_keyword(self):
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        for keyword in self.filter_fields():  
            # Get unique values from  index
            index = catalog._catalog.getIndex(keyword[0])
            if hasattr(index, 'uniqueValues'):
                filters.append({'name': keyword[0], 'title' : keyword[1], 'vals': sorted(index.uniqueValues())})
            
        return filters
    
    def get_filters(self):
        return api.portal.get_registry_record('filter_fields', interface=IProloogSettings)
        
   
    def filter_fields(self):
        factory = getUtility(IVocabularyFactory, name="medialog.hilversum.ProloogKeywords")
        vocab = factory(self.context)
        filter_list = []
        for field in api.portal.get_registry_record('filter_fields', interface=IProloogSettings):
            value = vocab.getTerm(field)
            filter_list.append([field, value])
        return filter_list
 
