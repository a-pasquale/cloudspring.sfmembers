from zope.interface import implements
from zope.interface import Interface
from zope import schema
from z3c.form import form, field, button
from plone.z3cform.layout import wrap_form
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

from sfmap import SFObject, SFField

import logging

logger = logging.getLogger('SF EditProfile')


class IContactInfo(Interface):
    """ Schema for member profile edit form """
    sf_id = schema.TextLine(title = u'Salesforce ID')
    name = schema.TextLine(title = u'Name')
    # etc...

class SFContact(SFObject):
    """ Adapts a Salesforce Account to the profile edit form schema"""
    implements(IContactInfo)

    _sObjectType = 'Contact'

    sf_id = SFField('sf_id__c')
    name = SFField('Name')
    # etc...

class EditProfileForm(form.Form):
    """ An edit form for the current authenticated member's Account """

    label = u'Update Profile'
    fields = field.Fields(IContactInfo)

    def _get_sf_id(self):
        """ Find the Salesforce Account Id corresponding to the current logged in member. """
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        sf_id = member.getProperty('sf_id')
        #sf_id = 'apasquale'
        if not sf_id:
            raise Exception("Did not find valid Salesforce ID for member '%s'" % member.getId())
        logger.info(type(sf_id))
        logger.info("Member sf_id = '%s'" % sf_id.__str__ )
        return sf_id

    def _sf_contact(self):
        sfbc = getToolByName(self.context, 'portal_salesforcebaseconnector')
        #return SFContact(sfbc, "sf_id__c='%s'" % self._get_sf_id())
        return SFContact(sfbc, "sf_id__c='%s'" % self._get_sf_id())

    @memoize
    def getContent(self):
        """ Provides the object this form will edit.
            Memoized so we always get the same one for a given request. """
        sfbc = getToolByName(self.context, 'portal_salesforcebaseconnector')
        #return SFContact(sfbc, "sf_id__c='%s'" % self._get_sf_id())
        return self._sf_contact()

    @button.buttonAndHandler(u'Update Profile')
    def handleUpdate(self, action):
        """ Handler for the Update Profile button """
        data, errors = self.extractData()
        if not errors:
            self.status = u'Changes saved.'
            # save changes to Salesforce
            sf_id = self._get_sf_id()
            sfbc = getToolByName(self.context, 'portal_salesforcebaseconnector')
            #SFContact.update(sfbc, id=sf_id, **data)

            SFContact.update(self._sf_contact(), id=sf_id, **data)

            # etc...additional code to update the local AT-based copy of the Account data...

EditProfileView = wrap_form(EditProfileForm)

