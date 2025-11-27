# -*- coding: utf-8 -*-

from plone.app.contenttypes.interfaces import IDocument
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer

from medialog.hilversum.content.proloog import  IProloog

@indexer(IDexterityContent)
def dummy(obj):
    """ Dummy to prevent indexing other objects thru acquisition """
    raise AttributeError('This field should not indexed here!')


@indexer(IProloog)  # ADJUST THIS!
def id(obj):
    """Calculate and return the value for the indexer
    There are bugs in CSV / Excel files, some ids are string some are float
    """
    value = obj.id
    
    # Float representing a whole number → "306"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    # Int → "306"
    if isinstance(value, int):
        return str(value)

    # Anything else → convert to string
    return str(value)
