# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form import interfaces
from zope import schema
#from zope.interface import Interface
from zope.interface import alsoProvides
from plone.supermodel import model
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from medialog.hilversum.keywords import get_keywords as keywords

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.hilversum')
                                  

class IMedialogHilversumLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""



class IProloogSettings(model.Schema):
    """Adds settings to medialog.controlpanel
    """

    model.fieldset(
        'Proloog',
        label=_(u'Prolog'),
        fields=[
            'table_fields',
            'filter_fields',
            'show_filter_icons', 
            ],
        )

    filter_fields = schema.List(
        title=u"Select Proloog Fields for filter viewlet",
        description=u"Select the filters you want for the viewlet",
        default=['aanbieder', 'themea'],
        required=False,
        value_type=schema.Choice(vocabulary='medialog.hilversum.PrologKeywords')
    )
    
    table_fields   = schema.List(
        title=u"Select Proloog Fields for table view",
        description=u"Select Table fields",
        default=['aanbieder', 'themea'],
        required=False,
        value_type=schema.Choice(vocabulary='medialog.hilversum.PrologKeywords')
    )
    
    show_filter_icons   = schema.Bool(
        title=u"Show filter icons",
        required=False,
    )

alsoProvides(IProloogSettings, IMedialogControlpanelSettingsProvider)

 