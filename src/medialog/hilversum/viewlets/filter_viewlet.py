# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from medialog.hilversum.keywords import get_keywords as keywords
from medialog.hilversum.keywords import get_discipline as discipline

# from medialog.hilversum.keywords import get_keyword as keyword



from urllib.parse import unquote


class FilterViewlet(ViewletBase):
            
    def index(self):
        return super(FilterViewlet, self).render()

    def update(self):
        self.keyword = self.get_keyword()
        self.keywords = self.get_keywords()
        self.site_url = self.site_url()
        
    def site_url(self):
        return api.portal.get().absolute_url()
        
    # get keyword by calling with  index name
    def get_discipline(self):
        return discipline(self)

    # get keyword by calling with all index name, as loop
    def get_keyword(self):
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        for keyword in self.get_keywords():  
            # import pdb; pdb.set_trace()          
            # Get unique values from  index
            index = catalog._catalog.getIndex(keyword[0])
            if hasattr(index, 'uniqueValues'):
                filters.append({'name': keyword[0], 'title' : keyword[1], 'vals': sorted(index.uniqueValues())})
            
        return filters
    
    def get_keywords(self):  
        return keywords(self)        
    
    # def get_filters(self):
    #     allowed_keys = {k for k, _ in self.get_keywords(self)}
    #     # Filter request.form for only those keys
    #     return [
    #         {'key': key, 'value': self.request.form.get(key)}
    #         for key in self.request.form
    #         if key in allowed_keys
    #     ]
        
    def get_filters(self):
        allowed_keys = {k for k, _ in self.get_keywords()}
        return {
            key: self.request.form.get(key)
            for key in self.request.form
            if key in allowed_keys
        }
