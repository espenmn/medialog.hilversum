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

import pandas as pd
from pandas import *
import openpyxl
 
#from bs4 import BeautifulSoup
#import re

def handler(obj, event):
    """ Event handler
    """
    #print(u"{0} on object {1}".format(event.__class__, obj.absolute_url()))

    excelfile = '/Users/rolf/Desktop/xxxl.xlsx'

    df = pd.read_excel('xxxl.xlsx')
    print(df)

    my_dict = df.to_dict(orient='index')


    #Main script here
    # Iterate the loop to read the cell values
    #in case we just want to rerun some
    for i in range(0, len(my_dict)):
        #
        # old_id = my_dict[i].get('ID old')
        the_dict = my_dict[i]


        # check if item exists
        # Add content if not
        # update fields
        # overwrite or not??
        
        #if item exists:
            #for key, value etc.
        
        for key, value in the_dict:
            #do something
            # check if item exists
            # add content
            # add fields by the loop

            a =1

        # brains = app.skipshistorie.portal_catalog(id=plone_id)

        # if brains:
        #     add_metadata(brains[0])
        # else:
        #     brains = app.skipshistorie.portal_catalog(portal_type="Document")
        #     transaction.commit()



    # def add_metadata(brain):
    #     obj = brain.getObject()
    #     for key, value in my_dict[i].items():
    #         #print(key)
    #         # if key=='type':
    #         #     key = 'skipstype'
    #         # if key=='del':
    #         #     key = 'del_'

    #         if value and str(value).lower() != 'nan':
    #             setattr(obj, key.lower().replace(" ", ""), value)
    #         else:
    #             #import pdb; import pdb; pdb.set_trace()
    #             setattr(obj, key.lower().replace(" ", ""), None)


    # if brains:
    #     print('Total  objects: ')
    #     print(len(brains))
    #     ant = 0
    #     ## Use reversed since maybe the last finished or not
    #     for brain in reversed(brains):

    #         #obj = brain.getObject()
    #         #main_folder = brain.getObject().getPhysicalPath()[2]
    #         #import pdb; pdb.set_trace()
    #         obj = brain.getObject()
    #         parent = get_first_folder(obj)
    #         #import pdb; pdb.set_trace()

    #         # check for document if we change things later
    #         if parent:
    #             if brain.portal_type == 'Document':
    #                 #Add tag from first folder
    #                 tags = obj.subject + (parent.Title(), )
    #                 print(parent.Title())
    #                 ant = ant+1
    #                 print(ant)
    #                 obj.subject =   tuple(set(tags))
    #                 modified(obj)


    print(ant)
    transaction.commit()
