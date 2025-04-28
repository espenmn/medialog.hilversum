# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


# from medialog.hilversum import _


class ICsvFile(model.Schema):
    """ Marker interface and Dexterity Python Schema for CsvFile
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('csv_file.xml')

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    directives.read_permission(csv_file='cmf.ManagePortal')
    directives.write_permission(csv_file='cmf.ManagePortal')
    
    csv_file = namedfile.NamedBlobFile(
        title=_(u'CSV File'),
        required=False,
    )


@implementer(ICsvFile)
class CsvFile(Item):
    """ Content-type class for ICsvFile
    """
