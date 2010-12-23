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

from AccessControl import allow_module
allow_module('cloudspring.sfmembers.createMemberArea')

MEMBER_SOBJECT_TYPE = 'Contact'
MEMBER_DIRECTORY = 'community/members'
MEMBER_DIRECTORY_ID = 'members'
MEMBER_PORTAL_TYPE = 'cloudspring.sfmembers.Member'
PUBLISH_ACTION = 'publish'
logger = logging.getLogger('Create Member Area')


def publish(context, item):
    wftool = getToolByName(context, 'portal_workflow')
    # publish and reindex
    try:
        logger.info("Publishing %s... " % item.Title)
        wftool.doActionFor(item, PUBLISH_ACTION)
    except:
        logger.info("Failed to publish %s" % item.Title)
        pass
    item.reindexObject(idxs=['Title'])

def getDirectoryFolder(context, dir):
    portal = getToolByName(context, 'portal_url').getPortalObject()
    cur_dir = portal.unrestrictedTraverse('')
    for d in dir:
        logger.info("d %s " % d)
        logger.info("curdir: %s" % cur_dir ) 
        try:
            cur_dir = cur_dir.unrestrictedTraverse(d)
        except (AttributeError, KeyError):
            logger.info("cur_dir: %s" % cur_dir)
            logger.info("Folder %s doesn't exist yet, so create it." % d)
            cur_dir.invokeFactory("Folder", d)
            logger.info("InvokeFactory %s " % d)
            cur_dir = getattr(cur_dir, d)
            cur_dir.setTitle(cur_dir.id.title())
            cur_dir.reindexObject(idxs=['Title'])
            publish(context, cur_dir)

    return cur_dir

def findOrCreateProfileById(context, name, id):

    member_dir_path = MEMBER_DIRECTORY.split("/")
    member_dir_path.append(id)
 
    directory = getDirectoryFolder(context, member_dir_path)
    dir = getattr(directory, id)

    # Change the title to the members fullname.
    home_dir = getattr(dir, id)
    home_dir.setTitle(name)

    # publish and reindex
    publish(context, home_dir)

    # look for the member's blog folder
    try:
        blog_folder = dir.unrestrictedTraverse('blog')
    except:
        dir.invokeFactory("Folder", 'blog')
    blog_folder = getattr(dir, 'blog')

    # Change ownership and give local roles to member folder
    acl_users = getToolByName(context, "acl_users")
    user = acl_users.getUserById(id)
    blog_folder.changeOwnership(user)
    blog_folder.__ac_local_roles__ = None
    blog_folder.manage_setLocalRoles(id, ['Owner'])

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
       blog_collection = dir.unrestrictedTraverse('blog-collection')
    except:
        blog_title = "%s's blog" % name
        dir.invokeFactory(id="blog-collection", type_name="Topic", title=blog_title)
    blog_collection = getattr(blog_folder, "blog-collection")
    theCriteria = blog_collection.addCriterion('path','ATRelativePathCriterion')
    theCriteria.setRelativePath("../blog")

    blog_collection.setLayout('blog_view')

    # Hide the collection from navigation.
    blog_collection.setExcludeFromNav(True)
    # publish and reindex
    publish(context, blog_collection)

    # set the default page for the home folder to the collection
    dir.setDefaultPage("blog-collection")

    # get the member profile object, if it exists.
    try:
        logger.info("Looking for the member profile...")
        profile = getattr(dir, "profile")
    except:
        logger.info("The profile doesn't exist, so create it.")
        profile_id = dir.invokeFactory("cloudspring.sfmembers.member", "profile")
        logger.info("Profile created.")
        profile = getattr(dir, profile_id)

    profile_title = "%s's profile" % name
    profile.setTitle(profile_title)
    logger.info("Profile.Title: %s" % profile.Title)
    # Hide the profile from navigation.
    profile.setExcludeFromNav(True)
    # Change ownership and give local roles to member profile
    profile.changeOwnership(user)
    profile.__ac_local_roles__ = None
    profile.manage_setLocalRoles(id, ['Owner'])

    logger.info('Creating %s' % '/'.join(profile.getPhysicalPath()))

    return profile

def updateProfile(context, profile, name, firstName, lastName, id, email, role):
    logger.info("Updating " + name)
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
 
