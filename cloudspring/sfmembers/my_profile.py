from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.interfaces import IMyProfilePortlet

from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _


class Assignment(base.Assignment):
    implements(IMyProfilePortlet)

    @property
    def title(self):
        return _(u"My Profile Portlet")


class AddForm(base.AddForm):
    form_fields = form.Fields(IMyProfilePortlet)
    label = _(u"Add My Profile Portlet")
    description = _(u"This portlet displays a members profile.")

    def create(self, data):
        return Assignment(self.context)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('my_profile.pt')
    
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()

    @memoize
    def _member(self):
       if self.anonymous: # the user has not logged in
           return None
       else:
           mt = getToolByName(self.context, 'portal_membership')
           member = mt.getAuthenticatedMember()
           username = member.getUserName()
           portal = getToolByName(self.context, 'portal_url').getPortalObject()
           profile = portal.members[username].profile
           return profile

    def getUrl(self):
        member = self._member()
        return member.aq_inner.aq_parent.absolute_url_path()

    def getFirstName(self):
        member = self._member()
        return member.firstName

    def getName(self):
        member = self._member()
        return member.name

    def getDiscipline(self):
        member = self._member()
        return member.discipline

    def getAcademicInterests(self):
        member = self._member()
        return member.academic_interests

    def getAddress(self):
        member = self._member()
        return member.address

    def getCity(self):
        member = self._member()
        return member.city

    def getState(self):
        member = self._member()
        return member.state

    def getZipcode(self):
        member = self._member()
        return member.zipcode

    def getPublicEmail(self):
        member = self._member()
        return member.email

    def getFacebook(self):
        member = self._member()
        return member.facebook

    def getWorkPhone(self):
        member = self._member()
        return member.work_phone

    def getTwitter(self):
        member = self._member()
        return member.twitter

    def getPicture(self):
        member = self._member()
        return member.picture

    def render(self):
        return self._template()

    @property
    def available(self):
        return not self.anonymous


