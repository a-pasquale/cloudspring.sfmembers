from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.interfaces import IProfilePortlet

from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


class Assignment(base.Assignment):
    implements(IProfilePortlet)

    def __init__(self, context):
       sf_id = context.getId()
       catalog = getToolByName(context, 'portal_catalog')
       results = catalog(id=sf_id)

       for member in results:
           self.name = member.Title
           self.url = "%s/profile" % member.getURL()

    @property
    def title(self):
        return _(u"Profile Portlet")


class AddForm(base.AddForm):
    form_fields = form.Fields(IProfilePortlet)
    label = _(u"Add Profile Portlet")
    description = _(u"This portlet displays a members profile.")

    def create(self, data):
        return Assignment(self.context)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('profile.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @memoize
    def _member(self):
        sf_id = self.context.getId()       
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(id=sf_id)
        for result in results:
            member = result.profile
            return member

    def getUrl(self):
        member = self._member()
        return "%s/profile" % member.getURL()

    def getName(self):
        member = self._member()
        return member.name

    def getProgram(self):
        member = self._member()
        return member.masters_program

    def getEmail(self):
        member = self._member()
        return member.email

    def getFacebook(self):
        member = self._member()
        return member.facebook

    def render(self):
        return self._template()

    @property
    def available(self):
        return True


