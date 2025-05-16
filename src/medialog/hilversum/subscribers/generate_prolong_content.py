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
from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
import datetime
from zope.schema import Date
from zope.schema import getFields

import pandas as pd
from io import BytesIO
from pandas import *
import openpyxl
import re
 
#from bs4 import BeautifulSoup
#import re

def handler(obj, event):
    """ Crete content from CSV file
    """
    
    blob = obj.csv_file  # This is a NamedBlobFile
    replace_content = obj.replace
    
    #disable 'replace setting' so it does not overwrite next time
    setattr(obj, 'replace_content', False)
    obj.reindexObject()

    if blob is not None:
        data = blob.data  # raw bytes
        #Check if it is excel or CSV or nothing
        if blob.filename.endswith('.xlsx') or blob.filename.endswith('.xls'):
            df = pd.read_excel(BytesIO(data))
        elif blob.filename.endswith('.csv'): 
            df = pd.read_csv(BytesIO(data), sep=';', engine='python')  # read CSV from bytes
        else:
            # Alternatively, we could try to read it  ( try: / except Exception: )
            pass

        print(df)
        my_dict = df.to_dict(orient='index')        
        portal = plone.api.portal.get()
        
        # 'Prolong' is the portal_type name
        fti = getUtility(IDexterityFTI, name='Prolong')
        
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
            "Datetime": Timestamp # Same here, use datetime.datetime if needed
        }

        # A  loop to read the cell values
        # check if item exists
        # Add content if not / # update fields / overwrite or not
            
        for i in range(0, len(my_dict)):
            the_dict = my_dict[i]
            the_title = str(the_dict['Naam'])
            the_id = str(the_dict['ID'])
            
            # Fields to use to add content and their names
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
                # "discipline" : the_dict["Discipline"],
                "discipline": the_dict["Leerlijn / Discipline"],
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
                # "max_aantal_leerlingen_prijsberekening" : the_dict["Max. aantal leerlingen prijsberekening"],
                # "totaalprijs" : the_dict["Totaalprijs"],
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
                "the_code" : the_dict["Code"], 
            }
            
            #Create content only if it does not exist
            item_exist = portal.get(the_id, False)            
            
            
            if not item_exist:
                prolong = plone.api.content.create(
                    type='Prolong',
                    title = the_title,
                    id = the_id,                
                    container=portal
                )
                
            else:
                prolong = portal.get(the_id)            
            
            if replace_content or not item_exist != False:
                # if replace_content or not item_exist:
                # import pdb; pdb.set_trace()
                # print( str(i) + ' : ' + the_title)
            
                for key, value in field_map.items():
                    print(str(i) + ' ' + key + " : " + str(value))
                    
                    if value and pd.notna(value) and value != "":
                        value_type = type(value)
                        field = getFields(schema)[key]
                        field_type = type(field).__name__   
                        # map bootstrap fields to comparable imported fields (types)
                        python_type = field_type_map.get(field_type, None)
                        
                        # Convert ints to string if field is string
                        if python_type == str:
                            value = str(value)
                        
                        # CSV file has wrong data format for some entries
                        # Excel file also has similar problems
                        if isinstance(value, datetime.datetime):
                            value = value.date()
                            
                        if value_type == Timestamp:        
                            # Convert to datetime.date
                            value = value.date()
                        
                        #due to bug 'bad csv files', we need to convert more dates 
                        #some dates have wrong syntax, need to fix them
                        if key in ['startdatum',  'einddatum' ] and isinstance(value, str):
                            # For unknow reason, the CSV users 0025 for year 2025 etc
                            value = value.replace("-00", "-20")
                            value = datetime.datetime.strptime(value, '%d-%m-%Y').date()                    
                        
                        #floats should be ints
                        if isinstance(value, float):
                            value = int(value)
                            # can remove this next line later
                            value_type = int
                            
                        #convert strings to list for 'list' fields
                        if python_type == list:
                            if isinstance(value, str):
                                value = re.split(r"[,\|]", value)
                                # can remove this next line later
                                value_type = list
                                                                
                        
                        # convert list of strings to list of ints for these
                        if key in ['tarief_leerling_groep']:
                            if value_type == list:
                                #Remove unset values
                                if 'nvt' in value:
                                    value.remove('nvt')
                                value = [int(x) for x in value]
                            else:
                                value = [value]
                        
                        #Not sure if leerjaren should be int, but it contains string ('ve')        
                        if key in ['leerjaren']:
                            if value_type == list:
                                #Remove unset values
                                value = [str(x) for x in value]
                            else:
                                value = str(value)
                                

                        if key == 'discipline':
                            subjekter = value
                            
                        #Create AAnbieder(s)
                        if key == 'aanbieder':
                            for item_name in value:
                                aan_id =   re.sub(r'[^a-z0-9]+', '-', item_name.lower()).strip('-')
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
                                if subjekter:
                                    aanbieder.setSubject(subjekter)                                 
                            
                        
                        setattr(prolong, key, value)  
                        
                # transaction.commit()  # TO DO, check if this is needed  
                prolong.setTitle(the_title)  
                prolong.reindexObject()  # Ensure catalog is updated for this Prolong 
                
    # obj.reindexObject()
        
