""""
Create a member area.

This script will create a member folder containing a profile and a blog folder.  Ownership of the blog folder is given to the member to allow posting.  A collection to display items posted in the blog folder is created and set to the default view for the member folder.

This script is designed to be triggered on the creation of a new plone member, or through a batch process where new members can be added in bulk.
"""

import logging
import transaction
from zope.component import getUtility
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import _createObjectByType
from zope.app.component.hooks import getSite
from cloudspring.sfmembers.member import IMember
import membership

from AccessControl import allow_module
allow_module('cloudspring.sfmembers.createMemberArea')

MEMBER_SOBJECT_TYPE = 'Contact'
MEMBER_DIRECTORY = 'members'
MEMBER_DIRECTORY_ID = 'members'
MEMBER_PORTAL_TYPE = 'cloudspring.sfmembers.Member'
PUBLISH_ACTION = 'publish-internally'
PUBLISHED_STATE = 'internally_published'
logger = logging.getLogger('Create Member Area')


def publish(context, item, state=PUBLISH_ACTION):
    wftool = getToolByName(context, 'portal_workflow')
    # publish and reindex
    try:
        logger.info("Publishing %s... " % item.Title)
        wftool.doActionFor(item, state)
    except:
        logger.info("Failed to publish %s" % item.Title)
        pass
    item.reindexObject(idxs=['Title'])

def getDirectoryFolder(context, id):
    try:
        # Get the members home folder.
        member_folder = membership.getBlog(context, id)
    except (AttributeError, KeyError):
        # Folder doesn't exist yet, so create it.
        logger.info("Folder doesn't exist yet, so create it.")
        portal = getToolByName(context, 'portal_url').getPortalObject()
        member_dir_path = MEMBER_DIRECTORY.split("/")
        members_dir = portal.unrestrictedTraverse(member_dir_path)
        members_dir.invokeFactory("Folder", id)
        logger.info("InvokeFactory %s " % id)
        member_folder = getattr(members_dir, id)
        member_folder.setTitle(member_folder.id.title())
        member_folder.reindexObject(idxs=['Title'])
        publish(context, member_folder)

    return member_folder

def findOrCreateProfileById(context, name, id):
    # Get the members folder
    dir = getDirectoryFolder(context, id)

    #dir = getattr(directory, id)

    # Change the title to the members fullname.
    dir.setTitle(name)

    # publish and reindex
    publish(context, dir)

    # look for the member's blog folder
    try:
        logger.info("Trying to get the blog folder.")
        blog_folder = dir['blog']
    except:
        logger.info("The blog folder doesn't exist.  Create it.")
        dir.invokeFactory("Folder", 'blog')
    blog_folder = dir['blog']

    # Change ownership and give local roles to member folder
    blog_folder.__ac_local_roles__ = None
    blog_folder.manage_setLocalRoles(id, ['Manager'])

    # This enables collective.blogging (I think).
    # Probably not necessary anymore?
    blog_field = blog_folder.getField('blog_folder')
    if blog_field:
        blog_field.set(blog_folder, True)

    # Hide the blog folder from navigation.
    blog_folder.setExcludeFromNav(True)

    # publish and reindex
    publish(context, blog_folder)

    # get the blog collection
    try:
       blog_collection = dir['blog-collection']
    except:
        blog_title = "%s's blog" % name
        dir.invokeFactory(id="blog-collection", type_name="Topic", title=blog_title)
    blog_collection = dir['blog-collection']
    # Most recent content is on top.
    try:
      theCriteria = blog_collection.addCriterion('path','ATRelativePathCriterion')
      theCriteria.setRelativePath("../blog")
      # Only show published content
      theCriteria = blog_collection.addCriterion('review_state','ATSimpleStringCriterion')
      theCriteria.setValue(PUBLISHED_STATE)
      sort_criteria = blog_collection.addCriterion('modified','ATSortCriterion')
      sort_criteria.setReversed(True)
    except:
      # criteria already set.
      pass

    blog_collection.setLayout('folder_summary_view')

    # Hide the collection from navigation.
    blog_collection.setExcludeFromNav(True)
    # publish and reindex
    publish(context, blog_collection)

    # set the default page for the home folder to the collection
    dir.setDefaultPage("blog-collection")

    # get the draft collection
    try:
       draft_collection = dir['drafts']
    except:
        dir.invokeFactory(id="drafts", type_name="Topic", title="Drafts")
    drafts_collection = dir['drafts']
    try: 
      # Set path to the blog directory
      theCriteria = drafts_collection.addCriterion('path','ATRelativePathCriterion')
      theCriteria.setRelativePath("../blog")
      # Only show drafts 
      theCriteria = drafts_collection.addCriterion('review_state','ATSimpleStringCriterion')
      theCriteria.setValue('private')
      # Sort the drafts so the most recent are first.
      sort_criteria = drafts_collection.addCriterion('modified','ATSortCriterion')
      sort_criteria.setReversed(True)
    except:
      # criteria already set.
      pass

    drafts_collection.setLayout('folder_summary_view')
    drafts_collection.__ac_local_roles__ = None
    drafts_collection.manage_setLocalRoles(id, ['Manager'])

    # get the member profile object, if it exists.
    try:
        logger.info("Looking for the member profile...")
        profile = dir['profile']
    except:
        logger.info("The profile doesn't exist, so create it.")
        profile_id = dir.invokeFactory("cloudspring.sfmembers.member", "profile")
        logger.info("Profile created.")
        profile = dir['profile']

    profile_title = "%s's profile" % name
    profile.setTitle(profile_title)
    logger.info("Profile.Title: %s" % profile.Title)
    # Hide the profile from navigation.
    profile.setExcludeFromNav(True)
    # Change ownership and give local roles to member profile
    profile.__ac_local_roles__ = None
    profile.manage_setLocalRoles(id, ['Editor'])

    logger.info('Creating %s' % '/'.join(profile.getPhysicalPath()))

    return profile

def updateProfile(context, profile, name, firstName, lastName, id, email, role):
    logger.info("Updating %s" % name)
    profile.sf_id = id
    profile.name = name
    profile.firstName = firstName
    profile.lastName = lastName
    profile.email = email
    profile.role = role

    # publish and reindex
    publish(context, profile)

def createMemberArea(context, name, firstName, lastName, id, email, role):
        """ Creates a member area including blog and profile
            for a plone memember 
        """
        logger.info('Starting CreateMemberArea')

        logger.info("Member name: %s, id: %s" % (name, id))

        profile = findOrCreateProfileById(context, name, id)
        logger.info("profile.Title: " + profile.title)
        updateProfile(context, profile, name, firstName, lastName, id, email, role)
        portal = getToolByName(context, 'portal_url').getPortalObject()

        # Create a collection to display a member directory.
        # Use the custom view for the collection,
        # and set it as the default page for the member folder.
        dir = membership.getBlog(context, id)
        parent = dir.aq_inner.aq_parent
        # get the members collection
        try:
            members_collection = parent['members-collection']
        except:
            parent.invokeFactory(id="members-collection", type_name="Topic")
        members_collection = parent['members-collection']
        try:
            theCriteria = members_collection.addCriterion('path','ATRelativePathCriterion')
            theCriteria.setRelativePath("..")
            theCriteria = members_collection.addCriterion('Type','ATPortalTypeCriterion')
            theCriteria.setValue("Folder")
        except:
            # criteria already set.
            pass

        members_collection.setLayout('member_summary_view')
        parent.setDefaultPage("members-collection")

        # Hide the collection from navigation.
        members_collection.setExcludeFromNav(True)
        # publish and reindex
        publish(context, members_collection)
 
        
