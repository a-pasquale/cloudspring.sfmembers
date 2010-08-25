"""
SFDC sync view. This is intended to be run via cron every night to update
the member profiles based on data from Salesforce.com.

It will:

 * Find all Accounts with a member status of 'Current' or 'Grace Period' (in
   our client's Salesforce schema this is a custom rollup field based on various
   criteria).

 * For each Account, find an existing Member Profile object in Plone whose
   'sf_id' field value equals the Id of the Account, and update it.

 * Or, if no existing Member Profile was found, create a new one and publish it.

 * Retract any existing Member Profiles that were no longer found as Accounts
   with the Active or Grace Period membership status in Salesforce, so they are
   still present but not publicly visible.

"""

import logging
import transaction
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import _createObjectByType
from plone.app.textfield.value import RichTextValue
from cloudspring.sfmembers.member import IMember
from cloudspring.sfmembers.organization import OrgMembers
from cloudspring.sfmembers.member import MemberOrgs


MEMBER_SOBJECT_TYPE = 'Contact'
MEMBER_FIELDS_TO_FETCH = (
    'sf_id__c',
    'Name',
    'FirstName',
    'LastName',
    '(SELECT aff.npe5__Organization__r.Name, aff.npe5__Role__c FROM Contact.npe5__Affiliations__r aff)',
    )
MEMBER_DIRECTORY_ID = 'community'
MEMBER_PORTAL_TYPE = 'cloudspring.sfmembers.member'

ORG_SOBJECT_TYPE = 'Account'
ORG_FIELDS_TO_FETCH = (
    'Name',
    '(SELECT aff.npe5__Contact__r.sf_id__c, aff.npe5__Contact__r.Name, aff.npe5__Role__c FROM Account.npe5__Affiliations__r aff)',
    )
ORG_DIRECTORY_ID = 'organizations'
ORG_PORTAL_TYPE = 'cloudspring.sfmembers.organization'

FETCH_CRITERIA = "Member_Status__c = 'Current' OR Member_Status__c = 'Grace Period'" 

logger = logging.getLogger('SFDC Import')

class UpdateMemberProfilesFromSalesforce(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        self.normalizer = getUtility(IIDNormalizer)

    def getDirectoryFolder(self, dir, id):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        # look for the global member folder
        try:
           member_dir = portal.unrestrictedTraverse(dir)
        except KeyError:
           # global member folder doesn't exist yet, so create it.
           portal.invokeFactory("Folder", dir)
           member_dir = getattr(portal, dir)
           member_dir.setTitle('Community')
           member_dir.reindexObject(idxs=['Title'])

        # look for the member's folder
        try: 
            directory = member_dir.unrestrictedTraverse(id)
        except:
             member_dir.invokeFactory("Folder", id)

        directory = getattr(member_dir, id)

        return directory

    def findOrCreateProfileBySfId(self, name, sf_id):
        res = self.catalog.searchResults(sf_id = sf_id)
        if res:
            # update existing profile
            profile = res[0].getObject()
            logger.info('Updating %s' % '/'.join(profile.getPhysicalPath()))
            return profile
        else:
            # didn't match sf_id or UID: create new profile
            #name = safe_unicode(name)
            #profile_id = self.normalizer.normalize(name)
            directory = self.getDirectoryFolder(MEMBER_DIRECTORY_ID, sf_id)
            dir = getattr(directory, sf_id)
            
            # Change ownership and give local roles to member folder
            acl_users = getToolByName(self, "acl_users")
            user = acl_users.getUserById(sf_id)
            dir.changeOwnership(user)
            dir.__ac_local_roles__ = None
            dir.manage_setLocalRoles(sf_id, ['Owner'])

            # Change the title to the members fullname.
            dir.setTitle(name)

            # Default view should be the blog view.
            dir.setLayout("blog-view")
            blog_field = dir.getField('blog_folder')
            if blog_field:
                blog_field.set(dir, True)
            
            # publish and reindex
            try:
                logger.info("Publishing %s's folder" % name )
                self.wftool.doActionFor(dir, 'publish')
            except:
                logger.info("Failed to publish %s's folder" % name)
                pass
            dir.reindexObject(idxs=['Title'])

            try: 
                profile = getattr(dir, "profile")
            except:
                # Create the member profile object.
                profile_id = dir.invokeFactory(MEMBER_PORTAL_TYPE, "profile")
                profile = getattr(dir, profile_id)
            
            profile.setTitle("profile")
            # Hide the profile from navigation.
            profile.setExcludeFromNav(True)
            # Change ownership and give local roles to member profile
            profile.changeOwnership(user)
            profile.__ac_local_roles__ = None
            profile.manage_setLocalRoles(sf_id, ['Owner'])

            profile.reindexObject(idxs=['Title'])

            logger.info('Creating %s' % '/'.join(profile.getPhysicalPath()))

        return profile

    def updateProfile(self, profile, data):
        logger.info("Updating " + data.Name)
        #profile.setTitle(data.sf_id__c)
        profile.sf_id = data.sf_id__c
        profile.name = data.Name
        profile.firstName = data.FirstName
        profile.lastName = data.LastName
        #profile.bio = RichTextValue(data.Biography__c, 'text/structured', 'text/html')
        organizations = []
        orgs = data.npe5__Affiliations__r
        logger.info("about to go through orgs")
        for org in orgs:
            name = org.npe5__Organization__r.Name
            id = safe_unicode(name)
            id = self.normalizer.normalize(id)

            role = org.npe5__Role__c
            logger.info("related org: " + name)
            organization = dict({"orgId": id,
                                 "orgName": name,
                                 "role": role})
            organizations.append(MemberOrgs(organization))

        profile.relatedOrganizations = organizations

        logger.info('profile.name: ' + profile.name)
        #profile.name(data.Name)
        #if not profile.getText():
        #    profile.setText(data.Description, mimetype='text/x-web-intelligent')
        #profile.setMailingAddress("%sn%s, %s %s" % (data.BillingStreet, data.BillingCity,
         #                                            data.BillingState, data.BillingPostalCode))
        # etc...

        # publish and reindex
        try:
            logger.info("Publishing " + profile.name)
            self.wftool.doActionFor(profile, 'publish')
        except:
            logger.info("Failed to publish " + profile.name)
            pass
        profile.reindexObject()

    def hideProfileBySfId(self, sf_id):
        res = self.catalog.searchResults(Title = sf_id)
        profile = res[0].getObject()
        try:
            self.wftool.doActionFor(profile, 'reject')
        except:
            pass

    def queryMembers(self):
        """ Returns an iterator over the records of active members from Salesforce.com """
        sfbc = getToolByName(self.context, 'portal_salesforcebaseconnector')
        where = '(' + FETCH_CRITERIA + ')'
        soql = "SELECT %s FROM %s WHERE %s" % (
            ','.join(MEMBER_FIELDS_TO_FETCH),
            MEMBER_SOBJECT_TYPE,
            where)
        logger.info(soql)
        res = sfbc.query(soql)
        logger.info('%s records found.' % res['size'])
        for member in res:
            yield member
        while not res['done']:
            res = sfbc.queryMore(res['queryLocator'])
            for member in res:
                yield member

    def findOrCreateOrgByName(self, name):
        res = self.catalog.searchResults(Title = name)
        if res:
            # update existing profile
            org = res[0].getObject()
            logger.info('Updating %s' % '/'.join(org.getPhysicalPath()))
            return org
        else:
            # didn't match sf_id or UID: create new profile
            name = safe_unicode(name)
            org_id = self.normalizer.normalize(name)
            portal_url = getToolByName(self.context, "portal_url")
            portal = portal_url.getPortalObject()
            directory = self.getDirectoryFolder(portal, ORG_DIRECTORY_ID)
            org_id = directory.invokeFactory(ORG_PORTAL_TYPE, org_id)
            org = getattr(directory, org_id)
            org.setTitle(name)
            org.reindexObject(idxs=['Title'])
            logger.info('Creating %s' % '/'.join(org.getPhysicalPath()))

        return org

    def updateOrg(self, org, data):
        logger.info("Updating " + data.Name)
        org.setTitle(data.Name)
        #profile.bio = RichTextValue(data.Biography__c, 'text/structured', 'text/html')
        members = []
        contacts = data.npe5__Affiliations__r
        for contact in contacts:
            id = contact.npe5__Contact__r.sf_id__c
            name = contact.npe5__Contact__r.Name
            role = contact.npe5__Role__c

            member = dict({"memberId": id,
                           "memberName": name,
                           "role": role})
            members.append(OrgMembers(member))
        org.relatedMembers = members 
        logger.info('org.Title: ' + org.title)

        # publish and reindex
        try:
            logger.info("Publishing " + org.title)
            self.wftool.doActionFor(org, 'publish')
        except:
            logger.info("Failed to publish " + org.title)
            pass
        org.reindexObject()

    def queryOrgs(self):
        """ Returns an iterator over the records of active members from Salesforce.com """
        sfbc = getToolByName(self.context, 'portal_salesforcebaseconnector')
        where = '(' + FETCH_CRITERIA + ')'
        soql = "SELECT %s FROM %s " % (
             ','.join(ORG_FIELDS_TO_FETCH),
             ORG_SOBJECT_TYPE)
        logger.info(soql)
        res = sfbc.query(soql)
        logger.info('%s records found.' % res['size'])
        for member in res:
            yield member
        while not res['done']:
            res = sfbc.queryMore(res['queryLocator'])
            for member in res:
                yield member


    def __call__(self, queryMembers=queryMembers, queryOrgs=queryOrgs):
        """ Updates the member directory based on querying Salesforce.com """

        # 0. get list of sf_ids for the profiles we already know about, so we
        # can keep track of which ones we need to make private
        #sf_ids_not_found = set(self.catalog.searchResults(object_provides=IMember.__identifier__))

        # 1. fetch active Member Profile records, update ones that match,
        #    and create new ones
        for i, data in enumerate(queryMembers(self)):
            logger.info('i = ' + str(i) + " sf_id = " + data.sf_id__c + " name = " + data.Name)
            profile = self.findOrCreateProfileBySfId(name = data.Name, sf_id = data.sf_id__c)
            logger.info("profile.Title: " + profile.title)
            self.updateProfile(profile, data)

            # commit periodically (every 10) to avoid conflicts
            #if not i % 10:
            #    transaction.commit()
            logger.info("Would be committing transactions here...")

            # keep track of which profiles we need to hide
            #try:
            #    logger.info("Removing " + data.sf_id__c + " from list of ids not found")
            #    sf_ids_not_found.remove(data.sf_id__c)
            #except KeyError:
            #    logger.info("error removing " + data.sf_id__c)
            #    pass

        # 2. hide any profiles that are no longer active
        #for sf_id in sf_ids_not_found:
        #    logger.info("Hiding " + sf_id)
        #    self.hideProfileBySfId(sf_id)
        #for i, data in enumerate(queryOrgs(self)):
        #    logger.info('i = ' + str(i) + " Name = " + data.Name)
        #    org = self.findOrCreateOrgByName(name = data.Name)
        #    logger.info("org.Title: " + org.title)
        #    self.updateOrg(org, data)

