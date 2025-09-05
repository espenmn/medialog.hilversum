# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from plone import api
from urllib.parse import urlencode, quote

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IFavoritenView(Interface):
    """ Marker Interface for IFavoritenView"""


class FavoritenView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('favoriten_view.pt')

    def __call__(self):
        # Implement your own actions:
        self.back_url = self.get_back_url()
        #self.portal_url = self.portal_url()
        self.favorites = self.get_favorites()
        self.favorites_list = self.get_favorites_list()
        self.favorites_ids = self.get_favorites_ids()
        self.share_url = self.get_share_url()
        self.shared_favorites = self.get_shared_favorites()
        return super().__call__()
        # return self.index()

    def get_favorites_list(self):
        items = self.get_favorites()
        #dont need check, will only render if get_favorites returns items
        if items:
            itemlist = [item.UID for item in items]
            return ",".join(itemlist)
        return None
         
    def get_favorites_ids(self):
        items = self.get_favorites()
        #dont need check, will only render if get_favorites returns items
        if items:
            itemlist = [item.extern_id if item.extern_id else item.id for item in items]
            return ",".join(itemlist)
        return None
         
    def get_back_url(self):
        request = self.request
        referrer = request.get('HTTP_REFERER', '')
        # Optionally, restrict to only internal URLs
        if referrer and self.context.portal_url() in referrer:
            return referrer
        return self.context.absolute_url()  # fallback 

    
    def get_shared_favorites(self):
        favorite_ids = self.request.form.get('favorite_ids')
        #add = self.request.form.get('add')
        if favorite_ids:
            return favorite_ids.split(",")
        return None

        #return bool(favorite_ids and add == '1')


    def get_favorites(self):
        request = self.request
        favorites_from_cookie = request.cookies.get("favorites", None)
        favorites_from_query = self.get_shared_favorites()
        fav_list = []       
        
        
        if favorites_from_cookie:
            fav_list.extend(favorites_from_cookie.split(","))
            # fav_list.extend([x.strip() for x in favorites_from_cookie.split(",")])
            
        if favorites_from_query:
            fav_list.extend(favorites_from_query)
            
            
        if not fav_list:
            return []

        
        # Assuming data-id is UUID or id; adapt as needed
        catalog = api.portal.get_tool("portal_catalog")
        results = catalog(UID=fav_list)  # Use UID=ids if data-id is UUID
        return results
        # OR use id=ids if you're storing shortnames

        # Sort according to the original order
        # uid_to_obj = {r.UID: r.getObject() for r in results}
        # return [uid_to_obj[uid] for uid in ids if uid in uid_to_obj]


    def portal_url(self):
        return api.portal.get().absolute_url()
    
    def get_share_url(self):
        base_url = f"{self.portal_url()}/favoriten-view"
        query = {
            'favorite_ids': self.favorites_list,
            'add': 1,
        }

        share_url = f"{base_url}?{urlencode(query)}"

        subject = "Mijn favorieten"
        # Add plain URL to be automatically clickable
        body = f"Bekijk mijn favorieten via deze link:\n{share_url}"

        mailto_link = f"mailto:?subject={quote(subject)}&body={quote(body)}"
        return mailto_link



 

 
