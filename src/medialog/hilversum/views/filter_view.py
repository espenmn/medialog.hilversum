# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from medialog.hilversum.keywords import get_keywords as keywords

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFilterView(Interface):
    """ Marker Interface for IFilterView"""


class FilterView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('filter_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.keyword = self.get_keyword()
        self.keywords = self.get_keywords()
        self.site_url = self.site_url()
        return super(FilterView, self).__call__()


    def site_url(self):
        return api.portal.get().absolute_url()
        
    # get keyword by calling with  index name
    def get_discipline(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        index = catalog._catalog.getIndex('discipline')
        if hasattr(index, 'uniqueValues'):
            return sorted(index.uniqueValues())
        return None


    # get keyword by calling with  index name
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
        
        
 
