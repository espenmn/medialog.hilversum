# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            "medialog.hilversum:uninstall",
        ]

    def getNonInstallableProducts(self):
        """Hide the upgrades package from site-creation and quickinstaller."""
        return ["medialog.hilversum.upgrades"]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    
    portal = api.portal.get()
            
    if not portal.get('aambieders-collection', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='aambieders-collection',
                title='Aanbod',
                layout="providers-view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['aanbieder', 'Aanbieder']},
                ]
        )
    
    if not portal.get('providers-collection', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='providers-collection',
                title='Providers',
                layout="full_view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['aanbieder', 'Aanbieder']},
                ]
        )
    
    if not portal.get('proloogs-collection', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='proloogs-collection',
                title='Proloogs',
                layout="full_view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Proloog', 'proloog']},
                ]
        )
        
    if not portal.get('proloog-collection', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='proloog-collection',
                title='Proloog Overview',
                layout="proloog-folder-view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Proloog', 'proloog']},
                ]
        )

#     if not portal.get('proloogs-collections', False):
#         collection =  api.content.create(
#                 type='Collection',
#                 container=portal,
#                 id='proloogs-collections',
#                 title='Proloog 2s',
#                 layout="proloogs-view",
#                 query = [
#                         {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Proloog', 'proloog']},
#                 ]
#         )
        

    if not portal.get('proloog-listing', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='proloog-listing',
                title='Proloog Lijstweergave',
                layout="proloog-listing",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['Proloog', 'proloog']},
                ]
        )    
        
        

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
