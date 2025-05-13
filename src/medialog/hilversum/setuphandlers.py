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
                title='Aambieders',
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
    
    if not portal.get('prolongs-collection', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='prolongs-collection',
                title='Prolongs',
                layout="full_view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['prolong', 'Prolong']},
                ]
        )

    if not portal.get('prolongs-collections', False):
        collection =  api.content.create(
                type='Collection',
                container=portal,
                id='prolongs-collections',
                title='Prolong 2s',
                layout="prolongs-view",
                query = [
                        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.any', 'v': ['prolong', 'Prolong']},
                ]
        )

def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
