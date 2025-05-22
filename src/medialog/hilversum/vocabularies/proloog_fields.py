# -*- coding: utf-8 -*-

# from plone import api
from medialog.hilversum import _
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from medialog.hilversum.content.proloog import IProloog  


class VocabItem(object):
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class ProloogFields(object):
    """
    """

    def __call__(self, context):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []

        #
        # create a list of SimpleTerm items:
        terms = []
        
        for name, field in sorted(IProloog.namesAndDescriptions()):
            label = field.title or name
            if name != 'ID':
                terms.append(SimpleTerm(value=name, token=name, title=label))
 

        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


ProloogFieldsFactory = ProloogFields()



 
 


        
 