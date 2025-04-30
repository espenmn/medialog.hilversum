# -*- coding: utf-8 -*-

#import pandas as pd
#import openpyxl
from zope.lifecycleevent import modified
import plone.api
from zope.component.hooks import setSite
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.lifecycleevent import modified
import transaction
import plone.api

import pandas as pd
from io import BytesIO
from pandas import *
import openpyxl
 
#from bs4 import BeautifulSoup
#import re

def handler(obj, event):
    """ Crete content from CSV file
    """
    
    blob = obj.csv_file  # This is a NamedBlobFile

    if blob is not None:
        data = blob.data  # raw bytes
        df = pd.read_excel(BytesIO(data))
        print(df)

        my_dict = df.to_dict(orient='index')
        
        portal = plone.api.portal.get()

        # Main script here
        # Iterate the loop to read the cell values
        
        # check if item exists
        # Add content if not
        # update fields
        # overwrite or not??
            
        for i in range(0, len(my_dict)):
            the_dict = my_dict[i]
            the_title = the_dict['Naam']
            the_id = str(the_dict['ID'])
            
            field_map = {
                "naam" : the_dict['Naam'],
                "the_type" : the_dict["Type"],
                "expertise_aanbod" : the_dict["Expertise aanbod"],
                "aantal_lessen" : the_dict["Aantal lessen"],
                "uitvoering_op_school" : the_dict["Uitvoering op school"],
                "speelvlak" : the_dict["Speelvlak"],
                "verduistering" : the_dict["Verduistering"],
                "opbouwtijd" : the_dict["Opbouwtijd"],
                "min_aantal_leerlingen" : the_dict["Min. aantal leerlingen"],
                "ruimte_op_school" : the_dict["Ruimte op school"],
                "clusters" : the_dict["Clusters"],
                "programma" : the_dict["Programma"],
                "discipline" : the_dict["Discipline"],
                "thema" : the_dict["Thema"],
                "lesmateriaal_url" : the_dict["Lesmateriaal URL"],
                "aanbieder" : the_dict["Aanbieder"],
                "bemiddelaar" : the_dict["Bemiddelaar"],
                "vaste_ruimte" : the_dict["Vaste ruimte"],
                "vaste_gezelschappen" : the_dict["Vaste gezelschappen"],
                "vaste_personen" : the_dict["Vaste personen"],
                "blokje_persoon_inplannen" : the_dict["Blokje persoon inplannen"],
                "schooljaar" : the_dict["Schooljaar"],
                "duur" : the_dict["Duur"],
                "max_aantal_leerlingen" : the_dict["Max. aantal leerlingen"],
                "onderwijstype" : the_dict["Onderwijstype"],
                "vo_typen" : the_dict["VO typen"],
                "leerjaren" : the_dict["Leerjaren"],
                "inschrijfbaar" : the_dict["Inschrijfbaar"],
                "prijs_per" : the_dict["Prijs per"],
                "tarief_leerling_groep" : the_dict["Tarief leerling/groep"],
                "tarief_begeleider" : the_dict["Tarief begeleider"],
                "max_aantal_leerlingen_prijsberekening" : the_dict["Max. aantal leerlingen prijsberekening"],
                "totaalprijs" : the_dict["Totaalprijs"],
                "omschrijving" : the_dict["Omschrijving"],
                "url_meer_informatie" : the_dict["Url meer informatie"],
                "startdatum" : the_dict["Startdatum"],
                "einddatum" : the_dict["Einddatum"],
                "notitie" : the_dict["Notitie"],
                "extra_info_bij_inschrijven" : the_dict["Extra info bij inschrijven"],
                "extra_info_in_communicatie" : the_dict["Extra info in communicatie"],
                "verstuur_evaluatiemail" : the_dict["Verstuur evaluatiemail"],
                "url_evaluatieformulier" : the_dict["Url evaluatieformulier"],
                "ondertekening_emails" : the_dict["Ondertekening emails"],
                "extern_id" : the_dict["Extern ID"],
                "code" : the_dict["Code"],
                "vinkje_materiaal" : the_dict["Vinkje materiaal"],
                "pakketten" : the_dict["Pakketten"],
                "volgeboekt" : the_dict["Volgeboekt"],
                "podia_musea" : the_dict["Podia/Musea"],
            }
            
            obj = plone.api.content.create(
                type='Prolong',
                title = the_title,
                id = the_id,                
                container=portal
            )
            
            for key, value in field_map.items():
                if value and pd.notna(value) and value != "":
                    setattr(obj, key, value)

        obj.reindexObject()  # Ensure catalog is updated
  
        transaction.commit()
