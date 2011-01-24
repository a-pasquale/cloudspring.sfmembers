from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.interfaces import IProfilePortlet

from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


class Assignment(base.Assignment):
    implements(IProfilePortlet)

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
        import re
        pattern = 'members/(\w*)'
        match = re.search(pattern, self.context.absolute_url())
        sf_id = match.group(1)

        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(id=sf_id)
        for result in results:
            member = result.profile
            return member

    def getUrl(self):
        member = self._member()
        return member.getURL()

    def getFirstName(self):
        member = self._member()
        return member.firstName

    def getName(self):
        member = self._member()
        return member.name

    def getCellPhone(self):
        member = self._member()
        return member.cell_phone

    def getEmail(self):
        member = self._member()
        return member.email

    def getWebsite(self):
        member = self._member()
        return member.website

    def render(self):
        return self._template()

    @property
    def available(self):
        return True


