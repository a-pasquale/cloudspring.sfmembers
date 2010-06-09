from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText

from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from z3c.form.interfaces import IObjectFactory

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from cloudspring.sfmembers import _
from cloudspring.sfmembers.member import IMember


class IOrgMembers(Interface):

    memberId = schema.TextLine(
             title = _(u"Member ID"),
             required = True)
  
    memberName = schema.TextLine(
             title = _(u"Member Name"),
             required = True)
  
    role = schema.TextLine(
        title = _(u"Role"),
        required = False)


class OrgMembers(object):
     implements(IOrgMembers)

     def __init__(self, value):
         self.memberId=value["memberId"]
         self.memberName=value["memberName"]
         self.role=value["role"]


class OrgMembersFactory(object):
     adapts(Interface, Interface, Interface, Interface)
     implements(IObjectFactory)

     def __init__(self, context, request, form, widget):
         pass

     def __call__(self, value):
         return OrgMembers(value)


class IOrganization(form.Schema):
    """A Salesforce Account representing a organization in Plone.
    """
    
    title = schema.TextLine(
            title=_(u"Organization Name"),
        )
    
    description = schema.Text(
            title=_(u"A short description"),
        )
    
    form.primary('detailedDescription')
    detailedDescription = RichText(
            title=_(u"Detailed description of the organization"),
            required=False
        )

    relatedMembers = schema.List(
        title =_(u'relatedMembers'),
        description = _(u"Members of this organization"),
        required = False,
        value_type=schema.Object(
            title=_(u"Member"),
            schema=IOrgMembers),
     )

class View(grok.View):
    grok.context(IOrganization)
    grok.require('zope2.View')

    def published_content(self):
        """Return a catalog search result of members content.
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(Creator=context.title,
                       sort_order='sortable_title')
