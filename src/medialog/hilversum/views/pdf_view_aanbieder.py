# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from weasyprint import HTML, default_url_fetcher
import requests
from plone import api
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from medialog.hilversum.views.aanbieder_view import AanbiederView

class IPDFView(Interface):
    """ Marker Interface for IPDFView"""


@implementer(IPDFView)
class PDFView(AanbiederView):
    # We might want to define different templates for different content types (?)
    # template = ViewPageTemplateFile('pdf_view.pt')

    def __call__(self):

        # Render a dedicated template for PDF
        # set in configure.zcml, use template if we need 'options'
        
        self.discipline_images = self.get_discipline_images()
        self.portal_url = self.get_portal_url()
        self.courses = self.get_courses()
        self.disciplines = self.get_disciplines()
        
        html = self.index()

        pdf = HTML(
            string=html,
            base_url=self.context.absolute_url()
        ).write_pdf()

        self.request.response.setHeader(
            "Content-Type",
            "application/pdf",
        )

        self.request.response.setHeader(
            "Content-Disposition",
            f'attachment; filename="{self.context.Title()}.pdf"',
        )

        return pdf
