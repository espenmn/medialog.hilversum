# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from plone import api

# Template is set in configure.zcml
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile



class IProlongFolderView(Interface):
    """ Marker Interface for IProlongFolderView"""


class ProlongFolderView(BrowserView):
    
    def __call__(self):
        # Implement your own actions:
        return super(ProlongFolderView, self).__call__()
    
    # get the icons so we can check if they exist for the current course
    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
    
    def portal_url(self):
        return api.portal.get().absolute_url()
        