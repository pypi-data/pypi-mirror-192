# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import lapis.member


class LapisMemberLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=lapis.member)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'lapis.member:default')


LAPIS_MEMBER_FIXTURE = LapisMemberLayer()


LAPIS_MEMBER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LAPIS_MEMBER_FIXTURE,),
    name='LapisMemberLayer:IntegrationTesting',
)


LAPIS_MEMBER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LAPIS_MEMBER_FIXTURE,),
    name='LapisMemberLayer:FunctionalTesting',
)


LAPIS_MEMBER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LAPIS_MEMBER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='LapisMemberLayer:AcceptanceTesting',
)
