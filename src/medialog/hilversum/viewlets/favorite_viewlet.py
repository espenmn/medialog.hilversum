# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from plone import api


class FavoriteViewlet(ViewletBase):

    def update(self):
        self.portal_url = self.get_site_url()
    
    
    def get_site_url(self):
        return api.portal.get().absolute_url()