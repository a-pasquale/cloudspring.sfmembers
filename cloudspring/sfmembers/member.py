from five import grok
from zope import schema

from plone.directives import form, dexterity
from rwproperty import getproperty, setproperty

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from OFS.Image import Image

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
    """
    """
    
    form.omitted('sf_id')
    sf_id = schema.TextLine(
            title=_(u"Salesforce ID"),
        )

    form.fieldset('personal',
            label=(u'Personal'),
            fields=['firstName','lastName','name','picture','discipline','academic_interests','personal_interests','favorite_quote','role']
        )

    form.fieldset('contact',
            label=(u'Contact Information'),
            fields=['home_phone','cell_phone','work_phone','private_email','public_email','facebook','twitter','address','city','state','zipcode']
        )
    
    form.fieldset('cv',
            label=(u'Curriculum Vitae'),
            fields=['education','honors','fellowships','research','training','presentations','publications','collaborations','affiliations','skills']
        )

    form.fieldset('statement_of_purpose',
            label=(u'Statement of Purpose'),
            fields=['statement_of_purpose']
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

    home_phone = schema.TextLine(
            title=_(u"Home Phone (will not be publically available)"),
            required=False
        )
    
    cell_phone = schema.TextLine(
            title=_(u"Cell Phone (will not be publically available)"),
            required=False,
        )

    work_phone = schema.TextLine(
            title=_(u"Work phone"),
            required=True,
        )

    private_email = schema.TextLine(
            title=_(u"Private email"),
            required=True,
        )

    public_email = schema.TextLine(
            title=_(u"Public email"),
            required=True,
        )

    address = schema.Text(
            title=_(u"Street address"),
            required=True,
        )

    city = schema.TextLine(
            title=_(u"City"),
            required=True,
        )

    state = schema.TextLine(
           title=_(u"State"),
           required=True,
           min_length=2,
           max_length=2,
        )

    zipcode = schema.TextLine(
           title=_(u"Zip code"),
           required=True,
        )

    facebook = schema.TextLine(
            title=_(u"Facebook"),
            required=False,
        )

    twitter = schema.TextLine(
            title=_(u"Your Twitter username"),
            required=False,
        )

    form.omitted('community_role')
    community_role = schema.Choice(
            title=_(u"Community Role"),
            values=[_(u"Administrator"), _(u"Alumni"), _(u"Collaborator"), _(u"Faculty"), _(u"Staff"), _(u"Student"),],
            required=True,
    )

    discipline= schema.Choice(
            title=_(u"Discipline"),
            values=[_(u"Astronomy"), _(u"Biology"), _(u"Chemistry"), _(u"Materials"), _(u"Physics"),],
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
          
    statement_of_purpose = RichText (
           title=_(u"Statement of Purpose"),
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

    form.omitted('relatedOrganizations')
    relatedOrganizations = schema.List(
        title =_(u'Organizations'),
        description = _(u"This person is a member of the following organizations:"),
        required = False,
        value_type=schema.Object(
            title=_(u"Organization"),
            schema=IMemberOrgs),
     )

    role = schema.Choice(
            title=_(u"Role"),
            values=[_(u"Students"), _(u"Faculty"), _(u"Staff"), _(u"Collaborators"), _(u"Teaching Fellows"), _(u"Center Fellows"), _(u"Research Fellows"), _(u"Teaching Assistants"),],
            required=False,
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

class EditForm(dexterity.EditForm):
    grok.context(IMember)

    description = _(u"")
    label = _(u"Edit your profile")   

    def applyChanges(self, data):
        changes = super(EditForm, self).applyChanges(data)
        props = { "email"    : self.context.public_email,
                  "fullname" : self.context.name,
                }  

        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties(mapping=props)

        #picture = Image(id=self.context.picture.filename, file=self.context.picture.read(), title=self.context.picture.filename)
        #picture.filename = self.context.picture.filename

        #if picture: 
            #mt.changeMemberPortrait(picture, str(member.getId()))
            #transaction.commit()

        return changes

