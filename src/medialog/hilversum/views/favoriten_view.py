# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFavoritenView(Interface):
    """ Marker Interface for IFavoritenView"""


class FavoritenView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('favoriten_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()


    def get_favorites(self):
        request = self.request
        cookie_value = request.cookies.get("favorites")
        if not cookie_value:
            return []

        ids = cookie_value.split(",")

        # Assuming data-id is UUID or id; adapt as needed
        catalog = api.portal.get_tool("portal_catalog")
        results = catalog(UID=ids)  # Use UID=ids if data-id is UUID
        # OR use id=ids if you're storing shortnames
        return results

        # Sort according to the original order
        # uid_to_obj = {r.UID: r.getObject() for r in results}
        # return [uid_to_obj[uid] for uid in ids if uid in uid_to_obj]
