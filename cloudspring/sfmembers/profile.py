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
        pattern = 'community/(.*)/'
        match = re.search(pattern, self.context.absolute_url())
        sf_id = match.group(1)

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

    def getDiscipline(self):
        member = self._member()
        return member.discipline

    def getEmail(self):
        member = self._member()
        return member.email

    def getFacebook(self):
        member = self._member()
        return member.facebook

    def getHomePhone(self):
        member = self._member()
        return member.home_phone

    def getCellPhone(self):
        member = self._member()
        return member.cell_phone

    def getTwitter(self):
        member = self._member()
        return member.twitter

    def render(self):
        return self._template()

    @property
    def available(self):
        return True


