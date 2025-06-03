# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import getUtility
from zope.schema.vocabulary import getVocabularyRegistry
# from medialog.hilversum.keywords import get_keywords as keywords
from medialog.hilversum.keywords import get_discipline as discipline

from medialog.hilversum.interfaces import IProloogSettings

# from medialog.hilversum.keywords import get_keyword as keyword
from urllib.parse import unquote


class FilterViewlet(ViewletBase):
            
    def index(self):
        return super(FilterViewlet, self).render()

    def update(self):
        self.keyword = self.get_keyword()
        self.keywords = self.get_keywords()
        self.site_url = self.site_url()

    def site_url(self):
        return api.portal.get().absolute_url()

    def get_discipline(self):
        return discipline(self)

    def get_keywords(self):
        """Return [(name, title), ...] using registry and vocabulary."""
        registry_names = api.portal.get_registry_record('filter_fields', interface=IProloogSettings)
        # vocab_name = 'medialog.hilversum.PrologKeywords'
        vocab = getVocabularyRegistry().get(self.context, "medialog.hilversum.PrologKeywords")

        keywords = []
        for name in registry_names:
            try:
                term = vocab.getTerm(name)
                title = term.title if hasattr(term, "title") else name
            except LookupError:
                title = name
            keywords.append((name, title))
        return keywords

    def get_keyword(self):
        """Return structure for filters: [{'name': ..., 'title': ..., 'vals': [...]}, ...]"""
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')

        for keyword in self.get_keywords():
            index_name = keyword[0]
            index = catalog._catalog.getIndex(index_name)
            if hasattr(index, 'uniqueValues'):
                filters.append({
                    'name': index_name,
                    'title': keyword[1],
                    'vals': sorted(index.uniqueValues())
                })
        return filters

    def get_filters(self):
        """Get filter values from request if allowed in keyword list."""
        allowed_keys = {k for k, _ in self.get_keywords()}
        return {
            key: self.request.form.get(key)
            for key in self.request.form
            if key in allowed_keys
        }
