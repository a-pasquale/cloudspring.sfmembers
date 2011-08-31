from plone.app.portlets.portlets import base
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.interfaces import IMyContentPortlet

from zope.formlib import form

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
import membership

class Assignment(base.Assignment):
    implements(IMyContentPortlet)

    @property
    def title(self):
        return _(u"My Content Portlet")


class AddForm(base.AddForm):
    form_fields = form.Fields(IMyContentPortlet)
    label = _(u"Add My Content Portlet")
    description = _(u"This portlet displays a members content and allows workflow state to be changed.")

    def create(self, data):
        return Assignment(self.context)


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('myContent.pt')

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

    def getContent(self):
        if self.anonymous:
            return
 
        context = aq_inner(self.context)
        home = membership.getHomePath(context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog.searchResults(
                    portal_type=('cloudspring.sfmembers.reflection', 'Blog Entry'), 
                    path={'query': home, 
                          'depth': 2}
        )
       
        contents = []
        for brain in results:
            contents.append(brain.getObject())
        return contents


    def render(self):
        return self._template()

    @property
    def available(self):
        return not self.anonymous


