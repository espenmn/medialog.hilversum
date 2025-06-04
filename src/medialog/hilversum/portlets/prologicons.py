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
from plone import api
from medialog.hilversum.keywords import get_discipline as discipline
from medialog.hilversum.interfaces import IProloogSettings

# from medialog.hilversum.keywords import get_keyword as keyword
from urllib.parse import unquote



class IProloogiconsPortlet(IPortletDataProvider):
    place_str = schema.Bool(
        title=_(u'Show description'),
        required=False,
    )


@implementer(IProloogiconsPortlet)
class Assignment(base.Assignment):
    schema = IProloogiconsPortlet

    def __init__(self, place_str='nothing'):
        self.place_str = place_str

    @property
    def title(self):
        return _(u'Icon Portlet')


class AddForm(base.AddForm):
    schema = IProloogiconsPortlet
    form_fields = field.Fields(IProloogiconsPortlet)
    label = _(u'Add Proloog Icon Portlet') 

    def create(self, data):
        return Assignment(
            place_str=data.get('place_str', False),
        )


class EditForm(base.EditForm):
    schema = IProloogiconsPortlet
    form_fields = field.Fields(IProloogiconsPortlet)
    label = _(u'Edit Proloog Icon Portlet')
    description = _(u'This portlet shows Proloog Icons.')


class Renderer(base.Renderer):
    schema = IProloogiconsPortlet
    _template = ViewPageTemplateFile('prologicons.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return self._template()

    def site_url(self):
        return api.portal.get().absolute_url()

    def get_discipline(self):
        return discipline(self) 