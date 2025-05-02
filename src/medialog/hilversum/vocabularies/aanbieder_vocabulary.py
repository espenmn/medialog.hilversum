# -*- coding: utf-8 -*-

# from plone import api
from medialog.hilversum import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName

class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class AanbiederVocabulary(object):
    """ Shows all Aanbieders
    """


@implementer(IVocabularyFactory)
class AanbiederVocabulary(object):
    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        
        # Get unique values from 'aanbieder' index
        index = catalog._catalog.getIndex('aanbieder')
        if hasattr(index, 'uniqueValues'):
            unique_values = index.uniqueValues()
        else:
            unique_values = []

        # Create terms and vocabulary
        terms = [SimpleTerm(value=u, token=str(u), title=str(u)) for u in unique_values]
        return SimpleVocabulary(terms)


AanbiederVocabularyFactory = AanbiederVocabulary()
