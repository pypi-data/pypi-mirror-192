# -*- coding: utf-8 -*-
from lapis.member.testing import LAPIS_MEMBER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class ForumPageIntegrationTest(unittest.TestCase):

    layer = LAPIS_MEMBER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_forum_page_schema(self):
        fti = queryUtility(IDexterityFTI, name='Forum Page')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Forum Page')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_forum_page_fti(self):
        fti = queryUtility(IDexterityFTI, name='Forum Page')
        self.assertTrue(fti)

    def test_ct_forum_page_factory(self):
        fti = queryUtility(IDexterityFTI, name='Forum Page')
        factory = fti.factory
        obj = createObject(factory)


    def test_ct_forum_page_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Forum Page',
            id='forum_page',
        )


        parent = obj.__parent__
        self.assertIn('forum_page', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('forum_page', parent.objectIds())

    def test_ct_forum_page_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Forum Page')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
