# -*- coding: utf-8 -*-

# from medialog.hilversum import _
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.component import getUtility
from plone.resource.interfaces import IResourceDirectory


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IProlongView(Interface):
    """ Marker Interface for IProlongView"""


class ProlongView(BrowserView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('prolong_view.pt')

    def __call__(self):
        # Implement your own actions:
        return self.index()
    
    def portal_url(self):
        return api.portal.get().absolute_url()
    
    # def aanbieders(self):
    #     context = self.context
    #     catalog = getToolByName(context, 'portal_catalog')
        
    #     # Get unique values from 'aanbieder' index
    #     index = catalog._catalog.getIndex('aanbieder')
    #     if hasattr(index, 'uniqueValues'):
    #         return  index.uniqueValues()
    #     else:
    #         return None
 
    # get keyword by calling with  index name
    def get_keyword(self, keyword):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        # Get unique values from 'aanbieder' index
        index = catalog._catalog.getIndex(keyword)
        if hasattr(index, 'uniqueValues'):
            return  sorted(index.uniqueValues())
        else:
            return None
        
        
    def courses(self):
        # return self.context.portal_catalog(portal_type=['Prolong']d)
        return self.context.portal_catalog(portal_type=['Prolong'], aanbieder=self.context.aanbieder)
   
    # get the icons so we can check if they exist for the current course
    def get_discipline_images(self):
        resource_dir = getUtility(IResourceDirectory, name='++plone++medialog.hilversum')
        return  resource_dir.listDirectory() 
        
        
    def get_keywords(self): 
        return {
                "discipline": "Discipline",  
                "the_type": "Type",
                "programma": "Programma",               
                "ruimte_op_school": "Ruimte op school",
                "thema": "Thema",
                "aanbieder": "Aanbieder",
                "bemiddelaar": "Bemiddelaar",
                "vaste_ruimte": "Vaste ruimte",
                "vaste_personen": "Vaste personen",
                "inschrijfbaar": "Inschrijfbaar",
                "naam": 'Naam',
                "expertise_aanbod": "Expertise aanbod",
                "aantal_lessen": "Aantal lessen",
                "uitvoering_op_school": "Uitvoering op school",
                "verduistering": "Verduistering",
                "opbouwtijd": "Opbouwtijd",
                "min_aantal_leerlingen": "Min. aantal leerlingen",
                "vaste_gezelschappen": "Vaste gezelschappen",
                "blokje_persoon_inplannen": "Blokje persoon inplannen",
                "schooljaar": "Schooljaar",
                "duur": "Duur",
                "max_aantal_leerlingen": "Max. aantal leerlingen",
                "onderwijstype": "Onderwijstype",
                "leerjaren": "Leerjaren",
                 "tarief_leerling_groep": "Tarief leerling/groep",
                "tarief_begeleider": "Tarief begeleider"
        }