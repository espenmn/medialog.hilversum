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


from medialog.hilversum.keywords import get_keywords as keywords
# from medialog.hilversum.keywords import get_discipline as discipline
from urllib.parse import unquote


class IProlongfilterPortlet(IPortletDataProvider):
    replace_fields = schema.List(
        title=u"Select Proloog Fields to overwrite",
        description=u"Select the fields to override.",
        default=['naam', 'omschrijving'],
        required=False,
        value_type=schema.Choice(vocabulary='medialog.hilversum.ProloogFields')
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

    # def create(self, data):
    #     return Assignment(
    #         replace_fields.get('place_str', 'delhi,in'),
    #     )


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

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements and
        not an anonymous user."""
        return not self.anonymous and self.keyword

    def site_url(self):
        return api.portal.get().absolute_url()
 
    @memoize   
    def get_keyword(self):
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')        
        for keyword in self.keywords:          
            # Get unique values from  index
            index = catalog._catalog.getIndex(keyword[0])
            if hasattr(index, 'uniqueValues'):
                filters.append({'name': keyword[0], 'title' : keyword[1], 'vals': sorted(index.uniqueValues())})            
        return filters

 