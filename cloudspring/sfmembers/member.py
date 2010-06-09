from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from z3c.form.interfaces import IObjectFactory

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility

from cloudspring.sfmembers import _


class IMemberOrgs(Interface):

    orgId = schema.TextLine(
             title = _(u"Organization ID"),
             required = True)

    orgName = schema.TextLine(
             title = _(u"Organization Name"),
             required = True)

    role = schema.TextLine(
        title = _(u"Role"),
        required = False)


class MemberOrgs(object):
     implements(IMemberOrgs)

     def __init__(self, value):
         self.orgId=value["orgId"]
         self.orgName=value["orgName"]
         self.role=value["role"]


class MemberOrgsFactory(object):
     adapts(Interface, Interface, Interface, Interface)
     implements(IObjectFactory)

     def __init__(self, context, request, form, widget):
         pass

     def __call__(self, value):
         return MemberOrgs(value)

class IMember(form.Schema):
    """A Salesforce Contact representing a member in Plone.
    """
    
    title = schema.TextLine(
            title=_(u"Name"),
        )
    
    description = schema.Text(
            title=_(u"A short summary"),
        )
    
    form.primary('bio')
    bio = RichText(
            title=_(u"Bio"),
            required=False
        )
    form.primary('picture')
    picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

    relatedOrganizations = schema.List(
        title =_(u'Organizations'),
        description = _(u"This person is a member of the following organizations:"),
        required = False,
        value_type=schema.Object(
            title=_(u"Organization"),
            schema=IMemberOrgs),
     )

class View(grok.View):
    grok.context(IMember)
    grok.require('zope2.View')

    def published_content(self):
        """Return a catalog search result of members content.
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(Creator=context.title,
                       sort_order='sortable_title')
