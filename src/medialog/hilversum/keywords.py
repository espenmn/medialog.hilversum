# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from plone import api

# get keyword by calling with  index name
def get_discipline(self):
    context = self.context
    catalog = getToolByName(context, 'portal_catalog')
    index = catalog._catalog.getIndex('discipline')
    if hasattr(index, 'uniqueValues'):
        return sorted(index.uniqueValues())
        # return [item.lstrip().item.rstrip().replace(' ', '_') for item in values]
    return None


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
                ["tarief_begeleider",  "Tarief begeleider"],
                ["vo_typen", "VO typen"]
        ]