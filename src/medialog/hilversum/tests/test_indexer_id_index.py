# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from medialog.hilversum.testing import MEDIALOG_HILVERSUM_FUNCTIONAL_TESTING
from medialog.hilversum.testing import MEDIALOG_HILVERSUM_INTEGRATION_TESTING

import unittest


class IndexerIntegrationTest(unittest.TestCase):

    layer = MEDIALOG_HILVERSUM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)


class IndexerFunctionalTest(unittest.TestCase):

    layer = MEDIALOG_HILVERSUM_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)
