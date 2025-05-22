# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from Products.Five.browser import BrowserView

from medialog.hilversum.keywords import get_keywords as keywords

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IproloogView(Interface):
    """ Marker Interface for IproloogView"""



class proloogView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('proloog_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def portal_url(self):
        return api.portal.get().absolute_url()
 
    # get keyword by calling with the specific index name (keyword)
    def get_keyword(self, keyword):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        # Get unique values from 'aanbieder' index
        index = catalog._catalog.getIndex(keyword)
        if hasattr(index, 'uniqueValues'):
            return  sorted(index.uniqueValues())
        else:
            return None
        
    def courses(self):
        # return self.context.portal_catalog(portal_type=['proloog']d)
        return self.context.portal_catalog(portal_type=['proloog'], aanbieder=self.context.aanbieder)
   
    # get the icons so we can check if they exist for the current course
    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
    
    def is_favorite(self):
        request = self.request
        cookie_value = request.cookies.get("favorites")
        if cookie_value:
            uids = cookie_value.split(",")
            return self.context.UID() in uids
        return None

    def get_keywords(self): 
        return keywords