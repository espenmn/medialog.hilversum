# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from plone.app.contenttypes.browser.collection import CollectionView
from zope.interface import Interface
from plone import api
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory
from medialog.hilversum.keywords import get_keywords
# from urllib.parse import urlencode

# from medialog.hilversum.keywords import get_discipline 

# Set in zcml
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProloogFolderView(Interface):
    """ Marker Interface for IProloogFolderView"""


class ProloogFolderView(CollectionView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('proloog_folder_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.discipline_images = self.get_discipline_images()
        self.portal_url = self.get_portal_url()
        self.filters = self.get_filters()        
        return super(ProloogFolderView, self).__call__()


    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
    
    def get_portal_url(self):
        return api.portal.get().absolute_url()
    
    def get_filters(self):
        allowed_keys = {k for k, _ in get_keywords(self)}

        # Filter request.form for only those keys
        return [
            {'key': key, 'value': self.request.form.get(key)}
            for key in self.request.form
            if key in allowed_keys
        ]
        
        
    
