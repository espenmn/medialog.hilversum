# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
# from zope.schema import ValidationError
import mimetypes

from medialog.hilversum import _



def validate_excel_file(value):
    content_type = value.contentType
    if content_type not in [
        'application/vnd.ms-excel',  # .xls
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'text/csv'  # .csv
    ]:
        raise Invalid(u"Only Excel files (.xls, .xlsx) and CSV files (.csv) are allowed.")
    return True


class ICsvFile(model.Schema):
    """ Marker interface and Dexterity Python Schema for CsvFile
    """
    directives.read_permission(csv_file='cmf.ManagePortal')
    directives.write_permission(csv_file='cmf.ManagePortal')
    
    csv_file = namedfile.NamedBlobFile(
        title=_(u'CSV File'),
        required=True,
        constraint=validate_excel_file,
    )
    
    replace = schema.Bool(
        title=_(u'Override existing values'),
        description=_(u'Should we replace existing values of content already added'),
        required=False,
        default=False,
    )

@implementer(ICsvFile)
class CsvFile(Item):
    """ Content-type class for ICsvFile
    """