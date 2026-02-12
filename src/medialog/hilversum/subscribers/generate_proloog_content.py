# -*- coding: utf-8 -*-

#import pandas as pd
#import openpyxl
from zope.lifecycleevent import modified
import plone.api
from zope.component.hooks import setSite
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.rfc822.interfaces import IPrimaryFieldInfo
import transaction
import plone.api
from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
import datetime
from zope.schema import Date
from zope.schema import getFields
from Products.CMFCore.utils import getToolByName


import pandas as pd
from io import BytesIO
from pandas import *
import openpyxl
import re
import chardet



def parse_date(value):
    date_formats = ['%d-%m-%Y', '%d/%m/%y', '%Y-%m-%d', '%m/%d/%y', '%d.%m.%Y']
    
    for fmt in date_formats:
        try:
            return datetime.datetime.strptime(value, fmt).date() 
            # return datetime.datetime.strptime(value, '%d-%m-%Y').date()   
        except ValueError:
            continue
    return None  # Return None if no formats match


def set_aanbieder_subjects(obj):
    catalog = getToolByName(obj, 'portal_catalog')
    index = catalog._catalog.getIndex('aanbieder')
    
    # First we need to clear the subject index
    brains = plone.api.content.find(portal_type='Aanbieder')
    for brain in brains:
        obj = brain.getObject()
        obj.setSubject([])  # Clear all subjects

    if hasattr(index, 'uniqueValues'):
        for aanbieder_name in sorted(index.uniqueValues()):
            
            # Find the Aanbieder object with matching Title
            aanbieder_brains = plone.api.content.find(
                portal_type='Aanbieder',
                Title=aanbieder_name
            )
            if aanbieder_brains:                
                aanbieder_obj = aanbieder_brains[0].getObject()

                # Find Proloog items that reference this aanbieder
                proloog_brains = catalog(
                    portal_type='Proloog',
                    aanbieder=aanbieder_name
                )

                for brain in proloog_brains:
                    discipline = getattr(brain, 'discipline', None)
                    
                    if discipline:
                        aanbieder_obj.setSubject(discipline)

                # Step 4: Set Subject of Aanbieder to these values
                aanbieder_obj.reindexObject(idxs=['Subject'])

                    



def handler(obj, event):
    """ Crete content from CSV file
    """
    
    blob = obj.csv_file  # This is a NamedBlobFile
    replace_content = obj.replace
    replace_fields = obj.replace_fields
    
    #disable 'replace setting' so it does not overwrite next time
    setattr(obj, 'replace_content', False)
    obj.reindexObject()
    changes = 0

    if blob is not None:
        data = blob.data  # raw bytes
        #Check if it is excel or CSV or nothing
        if blob.filename.endswith('.xlsx') or blob.filename.endswith('.xls'):
            df = pd.read_excel(BytesIO(data))
        elif blob.filename.endswith('.csv'): 
            # detect encoding
            result = chardet.detect(data)
            encoding = result['encoding']
            df = pd.read_csv(BytesIO(data), sep=';', engine='python', encoding=encoding)  # read CSV from bytes
        else:
            # Alternatively, we could try to read it  ( try: / except Exception: )
            pass

        print(df)
        my_dict = df.to_dict(orient='index')        
        portal = plone.api.portal.get()
        
        # 'proloog' is the portal_type name
        fti = getUtility(IDexterityFTI, name='Proloog')
        
        # Get schema to know what type the fields are
        schema = fti.lookupSchema()
        
        #Field types to map to compare them to imported data
        field_type_map = {
            "TextLine": str,
            "Text": str,
            "Int": int,
            "Float": float,
            "Bool": bool,
            "List": list,          
            "Tuple": tuple,
            "Date": Timestamp,  
            "RichText": RichTextValue,     
            "Datetime": Timestamp # Same here, use datetime.datetime if needed
            
        }

        # A  loop to read the cell values
        # check if item exists
        # Add content if not / # update fields / overwrite or not
            
        for i in range(0, len(my_dict)):
            the_dict = my_dict[i]
            the_title = str(the_dict['Naam'])
            
            if the_title == 'nan':
                continue 
            
            valuen = the_dict['ID']
            the_id = str(valuen)
             
            # Float → "306.0"
            if isinstance(valuen, float) and valuen.is_integer():
                the_id = str(int(valuen))

            # Int → "306"
            if isinstance(valuen, int):
                the_id = str(valuen)
                
            import pdb; pdb.set_trace()

            #aanbieder = None
            
            # Fields to use to add content and their names
            # Added fallback if they do not exist
            field_map = {
                "naam" : the_dict.get("Naam", None),
                "the_type" : the_dict.get("Type", None),
                "expertise_aanbod" : the_dict.get("Expertise aanbod", None),
                "aantal_lessen" : the_dict.get("Aantal lessen", None),
                "uitvoering_op_school" : the_dict.get("Uitvoering op school", None),
                "speelvlak" : the_dict.get("Speelvlak", None),
                "verduistering" : the_dict.get("Verduistering", None),
                "opbouwtijd" : the_dict.get("Opbouwtijd", None),
                "min_aantal_leerlingen" : the_dict.get("Min. aantal leerlingen", None),
                "ruimte_op_school" : the_dict.get("Ruimte op school", None),
                "clusters" : the_dict.get("Clusters", None),
                "programma" : the_dict.get("Programma", None),
                # "discipline" : the_dict.get("Discipline", None),
                # "discipline": the_dict.get("Leerlijn / Discipline", None),
                "discipline": the_dict.get("Leerlijn / Discipline") or the_dict.get("Discipline") or None, 
                "thema" : the_dict.get("Thema", None),
                "lesmateriaal_url" : the_dict.get("Lesmateriaal URL", None),
                "aanbieder" : the_dict.get("Aanbieder", None),
                "bemiddelaar" : the_dict.get("Bemiddelaar", None),
                "vaste_ruimte" : the_dict.get("Vaste ruimte", None),
                "vaste_gezelschappen" : the_dict.get("Vaste gezelschappen", None),
                "vaste_personen" : the_dict.get("Vaste personen", None),
                "blokje_persoon_inplannen" : the_dict.get("Blokje persoon inplannen", None),
                "schooljaar" : the_dict.get("Schooljaar", None),
                "duur" : the_dict.get("Duur", None),
                "max_aantal_leerlingen" : the_dict.get("Max. aantal leerlingen", None),
                "onderwijstype" : the_dict.get("Onderwijstype", None),
                "vo_typen" : the_dict.get("VO typen", None),
                "leerjaren" : the_dict.get("Leerjaren", None),
                "inschrijfbaar" : the_dict.get("Inschrijfbaar", None),
                "prijs_per" : the_dict.get("Prijs per", None),
                "tarief_leerling_groep" : the_dict.get("Tarief leerling/groep", None),
                "tarief_begeleider" : the_dict.get("Tarief begeleider", None),
                # "totaalprijs" : the_dict.get("Totaalprijs", None),
                "omschrijving" : the_dict.get("Omschrijving", None),
                "url_meer_informatie" : the_dict.get("Url meer informatie", None),
                "startdatum" : the_dict.get("Startdatum", None),
                "einddatum" : the_dict.get("Einddatum", None),
                "notitie" : the_dict.get("Notitie", None),
                "extra_info_bij_inschrijven" : the_dict.get("Extra info bij inschrijven", None),
                "extra_info_in_communicatie" : the_dict.get("Extra info in communicatie", None),
                "verstuur_evaluatiemail" : the_dict.get("Verstuur evaluatiemail", None),
                "pakketten" : the_dict.get("Pakketten", None),"" : the_dict.get("", None),
                "podia_musea" : the_dict.get("Podia/Musea", None),"" : the_dict.get("", None),
                "totaalprijs " : the_dict.get("Totaalprijs ", None),"" : the_dict.get("", None),
                "url_overzicht" : the_dict.get("Url overzicht", None),"" : the_dict.get("", None),
                "vinkje_materiaal" : the_dict.get("Vinkje materiaal", None),"" : the_dict.get("", None),
                "volgeboekt" : the_dict.get("Volgeboekt", None),"" : the_dict.get("", None),                
                "url_evaluatieformulier" : the_dict.get("Url evaluatieformulier", None),
                "ondertekening_emails" : the_dict.get("Ondertekening emails", None),
                "extern_id" : the_dict.get("Extern ID", None),
                "the_code" : the_dict.get("Code", None), 
            }
            
            #Create content only if it does not exist in root folder
            item_exist = portal.get(the_id, False)            
            
            
            if not item_exist:
                proloog = plone.api.content.create(
                    type='Proloog',
                    title = the_title,
                    id = the_id,                
                    container=portal
                )
                
            else:
                proloog = portal.get(the_id)  
                
                
            ## check for replace and IMPORTANT, that the content type is 'Proloog'
            if proloog.Type() == "Proloog" and (replace_content or not item_exist != False):
                # if replace_content or not item_exist:
                # print( str(i) + ' : ' + the_title)
                
                for key, value in field_map.items():
                    subjekter = None
                    # Replace only fields that are set in 'replace_fields'
                    if key in replace_fields or not item_exist != False:
                        if value and pd.notna(value) and value != "":
                            
                            #body text is a behavior
                            if key == 'omschrijving':
                                setattr(proloog, 'text', RichTextValue(value))
                                continue
                                
                        
                            value_type = type(value)
                            field = getFields(schema)[key]
                            field_type = type(field).__name__   
                            # map bootstrap fields to comparable imported fields (types)
                            python_type = field_type_map.get(field_type, None)
                            
                            if python_type == RichTextValue: 
                                value = RichTextValue(value)
                            
                            # Convert ints to string if field is string
                            if python_type == str:
                                value = str(value)                         
                                                  
                            # CSV file has wrong data format for some entries
                            # Excel file also has similar problems
                            if value_type == Timestamp and not isinstance(value, datetime.datetime):        
                                # Convert to datetime.date
                                value = value.date()
                                
                            if isinstance(value, datetime.datetime):
                                value = value.date()
                            
                            #due to bug 'bad csv files', we need to convert more dates 
                            #some dates have wrong syntax, need to fix them
                            if key in ['startdatum',  'einddatum' ] and isinstance(value, str):
                                # For unknow reason, the CSV users 0025 for year 2025 etc
                                value = value.replace("-00", "-20")
                                value = parse_date(value)                 
                            
                            #floats should be ints
                            if isinstance(value, float):
                                value = int(value)
                                # can remove this next line later
                                value_type = int
                                
                            if isinstance(value, str) and python_type == int:
                                value = int(value)  
                                
                            #convert strings to list for 'list' fields
                            if python_type == list:
                                if isinstance(value, str):
                                    value = re.split(r"[,\|]", value)
                                    # can remove this next line later
                                    value_type = list
                                                                    
                            
                            # convert list of strings to list of ints for these
                            # if key in ['tarief_leerling_groep']:
                            #     if value_type == list:
                            #         #Remove unset values
                            #         if 'nvt' in value:
                            #             value.remove('nvt')
                            #         value = [int(x) for x in value]
                            #     else:
                            #         value = [value]
                            if key in ['tarief_leerling_groep']:
                                if value_type == list:
                                    #Remove unset values
                                    if 'nvt' in value:
                                        value.remove('nvt')
                                    value = ",".join(value)
                                else:
                                    value = value
                            
                            #Not sure if leerjaren should be int, but it contains string ('ve')        
                            if key in ['leerjaren']:
                                if value_type == list:
                                    #Remove unset values
                                    value = [str(x) for x in value]
                                else:
                                    value = str(value)                                    
                            
                            if key == 'discipline':
                                value = [val.strip() for val in value]
                                
                            # Create Aanbieder(s)
                            if key == 'aanbieder':
                                value = [val.strip() for val in value]
                                for item_name in value:
                                    aan_id = re.sub(r'[^a-z0-9]+', '-', item_name.lower()).strip('-')
                                    if not portal.get(aan_id, False):
                                        aanbieder = plone.api.content.create(
                                            type='Aanbieder',
                                            title = item_name,
                                            id = aan_id,                
                                            container=portal
                                        )
                                    else:
                                        aanbieder = portal.get(aan_id)
                                    
                                    # subjects = list(aanbieder.Subject())
                                    #Add keywords to 'aanbieder'. Needs to be added after aanbieder is added
                                    #If this is not the 'order', we need to sort the list first /  TO DO / Check  
                                                          
                                                                    
                                
                            # update Proloog field 
                            setattr(proloog, key, value)  
                        else:
                            setattr(proloog, key, None)  
                            
                    changes += 1
                    
                # transaction.commit()  # TO DO, check if this is needed  
                proloog.setTitle(the_title)  
                proloog.reindexObject()  # Ensure catalog is updated for this proloog 
    
    # Update all Aanbieders with subject
    set_aanbieder_subjects(obj)
    message = "{} changes".format(changes) 
    plone.api.portal.show_message(message=message, request=None, type='info') 

                
    # obj.reindexObject()
        
