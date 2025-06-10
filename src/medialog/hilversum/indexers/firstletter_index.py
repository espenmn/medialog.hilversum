# -*- coding: utf-8 -*-

# from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from medialog.hilversum.content.aanbieder import IAanbieder


@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')

@indexer(IAanbieder) 
def firstletter_index(obj):
    """Calculate and return the value for the indexer, we need first letter for filters"""
    return obj.Title()[0]
