# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from weasyprint import HTML
from plone import api


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPDFView(Interface):
    """ Marker Interface for IPDFView"""


@implementer(IPDFView)
class PDFView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('pdf_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()



class AsPDF(BrowserView):

    def __call__(self):

        # Render a dedicated template for PDF
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
            f'attachment; filename="{self.context.id}.pdf"',
        )

        return pdf
