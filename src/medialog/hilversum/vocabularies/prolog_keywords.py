# -*- coding: utf-8 -*-

# from plone import api
from medialog.hilversum import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from medialog.hilversum.keywords import get_keywords as items

class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class ProloogKeywords(object):
    """
    """

    def __call__(self, context):        
        # create a list of SimpleTerm items:
        return  SimpleVocabulary([
                SimpleTerm(value=key, title=title) for key, title in items(self)
        ])


ProloogKeywordsFactory = ProloogKeywords()
