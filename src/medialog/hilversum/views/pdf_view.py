# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api
from weasyprint import HTML, default_url_fetcher
import requests


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from medialog.hilversum.views.proloog_view import ProloogView

class IPDFView(Interface):
    """ Marker Interface for IPDFView"""


def custom_fetcher(url):
    try:
        if url.startswith("http"):
            response = requests.get(url, timeout=10)
            return {
                "string": response.content,
                "mime_type": response.headers.get("Content-Type"),
            }
    except Exception:
        print(f"Failed to fetch: {url}")

    return default_url_fetcher(url)



@implementer(IPDFView)
class PDFView(ProloogView):
    # We might want to define different templates for different content types (?)
    # template = ViewPageTemplateFile('pdf_view.pt')

    def __call__(self):

        # Render a dedicated template for PDF
        # set in configure.zcml, use template if we need 'options'
        html = self.index()

        pdf = HTML(
            string=html,
            base_url=self.context.absolute_url(),
            url_fetcher=custom_fetcher
        ).write_pdf()
        
        # pdf = HTML(
        #     string=html,
        #     base_url=self.context.absolute_url()
        # ).write_pdf()


        self.request.response.setHeader(
            "Content-Type",
            "application/pdf",
        )

        self.request.response.setHeader(
            "Content-Disposition",
            f'attachment; filename="{self.context.Title()}.pdf"',
        )

        return pdf
