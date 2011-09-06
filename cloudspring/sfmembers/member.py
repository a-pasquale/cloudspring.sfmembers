from five import grok
from zope import schema

import z3c.form.form
import z3c.form.button
from Products.statusmessages.interfaces import IStatusMessage

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


class IMember(form.Schema):
    """
    """
    
    form.omitted('sf_id')
    sf_id = schema.TextLine(
            title=_(u"Salesforce ID"),
        )

    form.fieldset('general',
            label=(u'General'),
            fields=['firstName','lastName','name','picture','email','cell_phone','website','food_preferences','role']
        )

    form.fieldset('biography',
            label=(u'Biography'),
            fields=['place_of_birth','college_major','background','work_experiences','writing_projects','interests','leadership']
        )
    
    form.fieldset('education',
            label=(u'Education'),
            fields=['high_school','college','thesis','grad_school']
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

    cell_phone = schema.TextLine(
            title=_(u"Cell Phone"),
            required=False,
        )

    email = schema.TextLine(
            title=_(u"Email"),
            required=False,
        )

    website = schema.TextLine(
            title=_(u"Website (if you have one)"),
            required=False,
        )

    food_preferences = RichText(
            title=_(u"Food preferences and allergies"),
            required=False,
        )

    place_of_birth = schema.TextLine(
            title=_(u"Place of birth"),
            required=False,
        )

    college_major = schema.TextLine(
            title=_(u"College Major"),
            required=False,
        )

    background = RichText(
            title=_(u"Pre-law school relevant background: academic, personal or work experiences"),
            required=False
        )

    work_experiences = RichText(
           title=_(u"Work experiences in law school"),
           required=False,
        )

    writing_projects = RichText(
           title=_(u"Writing projects or articles in law school (other than this class)"),
           required=False,
        )

    interests = RichText(
           title=_(u"Interests and aspirations"),
           required=False,
        )

    leadership = RichText(
           title=_(u"Leadership and/or team experience"),
           required=False,
        )

    high_school = schema.TextLine (
            title=_(u"High school (was it public or private)"),
            required=False,
        )

    college = schema.TextLine (
            title=_(u"College (including your major)"),
            required=False,
        )

    thesis = schema.TextLine (
            title=_(u"Thesis or major paper in relevant areas (if any)"),
            required=False,
        )

    grad_school = schema.TextLine (
            title=_(u"Grad school (if any)"),
            required=False,
        )

    form.primary('picture')
    picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
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

    @getproperty
    def absolute_url(self):
        return self.absolute_url()

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

    @z3c.form.button.buttonAndHandler(_('Update profile'), name='update')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect(self.context.aq_parent.absolute_url())


    def applyChanges(self, data):
        changes = super(EditForm, self).applyChanges(data)
        props = { "email"    : self.context.email,
                  "fullname" : self.context.name,
                }  

        mt = getToolByName(self.context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        member.setMemberProperties(mapping=props)

        return changes

