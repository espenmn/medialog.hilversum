# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from medialog.hilversum.content.proloog import  IProloog
 
@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IProloog)
def vo_typen(obj):
    """Calculate and return the value for the indexer"""
    # attribute_name = "vo_typen"
    attribute_value = getattr(obj, "vo_typen", None)

    if not attribute_value:
        return None
    
    # Clean and filter values
    result = [
        x.strip().replace('-', ' ').replace('‚Äì', ' ').replace('  ', ' ')
        for x in attribute_value
        if x and x.strip()
    ]
    
    obj.vo_typen = result
    
    return result or None