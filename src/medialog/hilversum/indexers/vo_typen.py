# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IDocument)  # ADJUST THIS!
def vo_typen(obj):
    """Calculate and return the value for the indexer"""
    attribute_value = None
    attribute_name = "vo_typen"

    attribute_value = getattr(obj, attribute_name)
    if not attribute_value:
        return attribute_value
    return attribute_value
