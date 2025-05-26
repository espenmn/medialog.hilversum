# -*- coding: utf-8 -*-
from __future__ import absolute_import
from Acquisition import aq_inner
from medialog.hilversum import _
from plone import schema
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


from medialog.hilversum.keywords import get_keywords as keywords
# from medialog.hilversum.keywords import get_discipline as discipline
from urllib.parse import unquote


class IProlongfilterPortlet(IPortletDataProvider):
    replace_fields = schema.List(
        title=u"Select Proloog Fields for filters",
        description=u"Select the filters you want",
        default=['aanbieder', 'themea'],
        required=False,
        value_type=schema.Choice(vocabulary='medialog.hilversum.PrologKeywords')
    )


@implementer(IProlongfilterPortlet)
class Assignment(base.Assignment):
    schema = IProlongfilterPortlet

    def __init__(self, replace_fields=[]):
        self.replace_fields = replace_fields

    @property
    def title(self):
        return _(u'Filters')


class AddForm(base.AddForm):
    schema = IProlongfilterPortlet
    form_fields = field.Fields(IProlongfilterPortlet)
    label = _(u'Add Filters')
    description = _(u'This portlet displays Filters.')

    def create(self, data):
        return Assignment(
            replace_fields = data.get('replace_fields', []),
    )
        
class EditForm(base.EditForm):
    schema = IProlongfilterPortlet
    form_fields = field.Fields(IProlongfilterPortlet)
    label = _(u'Edit Filters')
    description = _(u'This portlet displays filters')


class Renderer(base.Renderer):
    schema = IProlongfilterPortlet
    _template = ViewPageTemplateFile('prolongfilter.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        self.keywords = keywords(self)
        self.site_url = self.site_url()
        # self.discipline = discipline()
        self.anonymous = portal_state.anonymous()
        self.keyword = self.get_keyword()
        self.filter_fields  = self.filter_fields()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements and
        not an anonymous user."""
        return not self.anonymous and self.keyword

    def filter_fields(self):
        factory = getUtility(IVocabularyFactory, name="medialog.hilversum.PrologKeywords")
        vocab = factory(self.context)
        filter_list = []
        for field in self.data.replace_fields:
            value = vocab.getTerm(field)
            filter_list.append(value)
        return filter_list
    
    def site_url(self):
        return api.portal.get().absolute_url()
 
    @memoize   
    def get_keyword(self):
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')     
        for keyword in self.filter_fields():          
            # Get unique values from  index
            index = catalog._catalog.getIndex(keyword.value)
            if hasattr(index, 'uniqueValues'):
                filters.append({'name': keyword.value, 'title' : keyword.title, 'vals': sorted(index.uniqueValues())})            
        return filters
    
    
    

 