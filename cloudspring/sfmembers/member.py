from five import grok
from zope import schema

from plone.directives import form, dexterity
from rwproperty import getproperty, setproperty

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from z3c.form.interfaces import IObjectFactory

from plone.dexterity.content import Item

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
    
    sf_id = schema.TextLine(
            title=_(u"Salesforce ID"),
        )
    
    firstName = schema.TextLine(
            title=_(u"First name"),
        )

    lastName = schema.TextLine(
            title=_(u"Last name"),
        )

    name = schema.TextLine(
            title=_(u"Full name"),
            default=_(u"Full Name"),
        )

    current_street = schema.TextLine(
            title=_(u"Street"),
        )

    current_city = schema.TextLine(
            title=_(u"City"),
        )

    current_state = schema.TextLine(
            title=_(u"State")
        )

    current_postal_code = schema.TextLine(
            title=_(u"Postal Code")
        )

    current_country = schema.TextLine(
            title=_(u"Country")
        )
     
    home_city = schema.TextLine(
            title=_(u"Hometown"),
            required=False
        )

    home_state = schema.TextLine(
            title=_(u"Home State"),
            required=False
        )

    home_country = schema.TextLine(
            title=_(u"Country of origin"),
            required=False
        )
     
    home_phone = schema.TextLine(
            title=_(u"Home Phone"),
            required=False,
        )
    
    cell_phone = schema.TextLine(
            title=_(u"Cell Phone"),
            required=False,
        )


    email = schema.TextLine(
            title=_(u"Email"),
            required=False,
        )

    facebook = schema.TextLine(
            title=_(u"Facebook"),
            required=False,
        )

    twitter = schema.TextLine(
            title=_(u"Twitter"),
            required=False,
        )

    masters_program = schema.Choice(
            title=_(u"Master's Program"),
            values=[_(u"Astronomy"), _(u"Biology"), _(u"Chemistry"), _(u"Physics"),],
            required=False,
        )

    academic_interests = schema.List(
            title=_(u"Academic Interests"),
            value_type=schema.Choice(values=[_(u"Research"), _(u"Teaching"),]),
            required=False,
        )

    education = RichText (
            title=_(u"Education"),
            required=False,
        )

    honors = RichText (
            title=_(u"Honors and Awards"),
            required=False,
        )

    fellowships = RichText (
            title=_(u"Fellowships and Grants"),
            required=False,
        )

    research = RichText (
            title=_(u"Research Experience"),
            required=False,
        )

    training = RichText (
            title=_(u"Training, Development and Mentoring Experience"),
            required=False,
        )

    presentations = RichText (
           title=_(u"Presentations"),
           required=False,
        )

    publications = RichText (
           title=_(u"Other Publications and Dissemination"),
           required=False,
        )

    collaborations = RichText (
           title=_(u"Collaborating Researchers and Institutions"),
           required=False,
        )

    affiliations = RichText (
           title=_(u"Professional Memberships and Affiliations"),
           required=False,
        )

    skills = RichText (
           title=_(u"Skills"),
           required=False,
        )

    contributions_within_discipline = RichText (
           title=_(u"Contributions within Discipline"),
           required=False,
        )

    contributions_to_other_disciplines = RichText (
           title=_(u"Contributions to other Disciplines"),
           required=False,
        )

    contributions_to_hr = RichText (
           title=_(u"Contributions to Human Resource Development"),
           required=False,
        )

    contributions_to_resources = RichText (
           title=_(u"Contributions to Resources for Research and Education"),
           required=False,
        )

    contributions_beyond = RichText (
           title=_(u"Contributions beyond Science and Engineering"),
           required=False,
        )

    aspirations = RichText(
            title=_(u"Future Goals, Research Interests and Aspirations"),
            required=False,
        )

    favorite_quote = RichText(
            title=_(u"Favorite quote"),
            required=False,
        )

    personal_interests = RichText(
            title=_(u"Personal Interests"),
            required=False,
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

class Member(Item):
    implements(IMember)

    def __init__(self, context):
        self.context = context

    @getproperty
    def name(self):
        return self.name

    @setproperty
    def name(self, value):
        self.context.name = value

class View(grok.View):
    grok.context(IMember)
    grok.require('zope2.View')

    def published_content(self):
        """Return a catalog search result of members content.
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(Creator=context.sf_id,
                       sort_order='sortable_title')
