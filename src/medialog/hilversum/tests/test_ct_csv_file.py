# -*- coding: utf-8 -*-
from medialog.hilversum.content.csv_file import ICsvFile  # NOQA E501
from medialog.hilversum.testing import MEDIALOG_HILVERSUM_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class CsvFileIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_HILVERSUM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_csv_file_schema(self):
        fti = queryUtility(IDexterityFTI, name='CsvFile')
        schema = fti.lookupSchema()
        self.assertEqual(ICsvFile, schema)

    def test_ct_csv_file_fti(self):
        fti = queryUtility(IDexterityFTI, name='CsvFile')
        self.assertTrue(fti)

    def test_ct_csv_file_factory(self):
        fti = queryUtility(IDexterityFTI, name='CsvFile')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICsvFile.providedBy(obj),
            u'ICsvFile not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_csv_file_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='CsvFile',
            id='csv_file',
        )

        self.assertTrue(
            ICsvFile.providedBy(obj),
            u'ICsvFile not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('csv_file', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('csv_file', parent.objectIds())

    def test_ct_csv_file_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='CsvFile')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
