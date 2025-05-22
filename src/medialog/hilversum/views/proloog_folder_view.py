# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface
from plone import api
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProloogFolderView(Interface):
    """ Marker Interface for IProloogFolderView"""


class ProloogFolderView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('proloog_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        return super(ProloogFolderView, self).__call__()


    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
    
    def portal_url(self):
        return api.portal.get().absolute_url()
        