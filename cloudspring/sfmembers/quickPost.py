from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.interfaces import IQuickPostPortlet

from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
import membership

class Assignment(base.Assignment):
    implements(IQuickPostPortlet)

    @property
    def title(self):
        return _(u"Quick-Post Portlet")


class AddForm(base.AddForm):
    form_fields = form.Fields(IQuickPostPortlet)
    label = _(u"Add Quick-Post Portlet")
    description = _(u"This portlet allows members to make quick posts.")

    def create(self, data):
        return Assignment(self.context)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('quickPost.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        #whether or not the current user is Anonymous
        self.anonymous = portal_state.anonymous()  

    @memoize 
    def getUrl(self):
        url = membership.getHomeUrl(self.context)
        return url

    def render(self):
        return self._template()

    @property
    def available(self):
        return not self.anonymous


