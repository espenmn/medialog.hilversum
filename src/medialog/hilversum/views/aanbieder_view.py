# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
# from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from plone import api

# Template is set in configure.zcml
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IAanbiederView(Interface):
    """ Marker Interface for IAanbiederView"""


class AanbiederView(BrowserView):
    
    b_size = 3
    
    def __call__(self):
        # Implement your own actions:
        self.discipline_images = self.get_discipline_images()
        self.portal_url = self.get_portal_url()
        self.courses = self.get_courses()
        self.disciplines = self.get_disciplines()
        return self.index()
    
    # get the icons so we can check if they exist for the current course
    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
    
    def get_portal_url(self):
        return api.portal.get().absolute_url()
    
    def get_courses(self):
        return self.context.portal_catalog(portal_type=['Proloog'], aanbieder=self.context.Title())
        
    def get_disciplines(self):
        prologs = self.courses
        disciplines = []
        for brain in prologs:
            if hasattr(brain, 'discipline') and brain.discipline:
                disciplines.extend(brain.discipline)
        return sorted(list(set(disciplines)))
           