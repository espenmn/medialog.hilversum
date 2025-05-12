# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName



class FilterViewlet(ViewletBase):

    def update(self):
        self.keyword = self.get_keyword()
        self.keywords = self.get_keywords()

    # get keyword by calling with  index name
    def get_discipline(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        index = catalog._catalog.getIndex('discipline')
        if hasattr(index, 'uniqueValues'):
            return sorted(index.uniqueValues())
        return None


    # get keyword by calling with  index name
    def get_keyword(self):
        filters = []
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        
        for keyword in self.get_keywords():  
            # import pdb; pdb.set_trace()          
            # Get unique values from  index
            index = catalog._catalog.getIndex(keyword[0])
            if hasattr(index, 'uniqueValues'):
                filters.append({'name': keyword[0], 'title' : keyword[1], 'vals': sorted(index.uniqueValues())})
            
        return filters
        
    def get_keywords(self): 
        return [
                ["discipline",  "Discipline"],  
                ["the_type",  "Type"],
                ["programma",  "Programma"],               
                ["ruimte_op_school",  "Ruimte op school"],
                ["thema",  "Thema"],
                ["aanbieder",  "Aanbieder"],
                ["bemiddelaar",  "Bemiddelaar"],
                ["vaste_ruimte",  "Vaste ruimte"],
                ["vaste_personen",  "Vaste personen"],
                ["inschrijfbaar",  "Inschrijfbaar"],
                ["naam",  'Naam'],
                ["expertise_aanbod",  "Expertise aanbod"],
                ["aantal_lessen",  "Aantal lessen"],
                ["uitvoering_op_school",  "Uitvoering op school"],
                ["verduistering",  "Verduistering"],
                ["opbouwtijd",  "Opbouwtijd"],
                ["min_aantal_leerlingen",  "Min. aantal leerlingen"],
                ["vaste_gezelschappen",  "Vaste gezelschappen"],
                ["blokje_persoon_inplannen",  "Blokje persoon inplannen"],
                ["schooljaar",  "Schooljaar"],
                ["duur",  "Duur"],
                ["max_aantal_leerlingen",  "Max. aantal leerlingen"],
                ["onderwijstype",  "Onderwijstype"],
                ["leerjaren",  "Leerjaren"],
                ["tarief_leerling_groep",  "Tarief leerling/groep"],
                ["tarief_begeleider",  "Tarief begeleider"]
        ]
        
        
    def index(self):
        return super(FilterViewlet, self).render()
