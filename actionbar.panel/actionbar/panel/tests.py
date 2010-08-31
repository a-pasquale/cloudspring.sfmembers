import unittest
from zope import component

from Testing import ZopeTestCase as ztc

from Products.Archetypes.Schema.factory import instanceSchemaFactory
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer

from plone import browserlayer

from actionbar.panel.browser.viewlets import ActionbarPanelViewlet
from actionbar.panel.browser.viewlets import HomeViewlet
from actionbar.panel.browser.viewlets import UserViewlet
from actionbar.panel.browser.viewlets import PersonalizeViewlet
from actionbar.panel.browser.viewlets import MembersViewlet
from actionbar.panel.browser.viewlets import NewsViewlet
from actionbar.panel.browser.interfaces import IActionbarPanelLayer

import actionbar.panel
ztc.installProduct('actionbar.panel')
ztc.installPackage(actionbar.panel)
SiteLayer = layer.PloneSite

class ActionbarPanelLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        PRODUCTS = ['actionbar.panel', ]
        ptc.setupPloneSite(products=PRODUCTS)

        fiveconfigure.debug_mode = True
        zcml.load_config('configure.zcml', actionbar.panel)
        fiveconfigure.debug_mode = False

        browserlayer.utils.register_layer(
                                IActionbarPanelLayer, 
                                name='actionbar.panel')

        component.provideAdapter(instanceSchemaFactory)
        SiteLayer.setUp()

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    layer = ActionbarPanelLayer


class TestViewlets(TestCase):
    """ """

    def test_actionbar.panelviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = ActionbarPanelViewlet(context, request, None, None)
        # XXX: This throws a componentProviderLookupError, so for some reason
        # the ActionbarPanelViewletManager is not being registered for the tests.
        # I, however, have no idea why :(
        # self.assertEqual(type(viewlet.render(), str))

    def test_homeviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = HomeViewlet(context, request, None, None)
        viewlet.update()

    def test_userviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = UserViewlet(context, request, None, None)
        viewlet.update()

    def test_personalizeviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = PersonalizeViewlet(context, request, None, None)
        viewlet.update()

    def test_membersviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = MembersViewlet(context, request, None, None)
        viewlet.update()

    def test_newsviewlet(self):
        """ """
        request = self.app.REQUEST
        context = self.portal
        viewlet = NewsViewlet(context, request, None, None)
        viewlet.update()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestViewlets))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


