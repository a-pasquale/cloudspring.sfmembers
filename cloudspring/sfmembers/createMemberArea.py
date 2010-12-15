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
from cloudspring.sfmembers.member import IMember

MEMBER_SOBJECT_TYPE = 'Contact'
MEMBER_DIRECTORY = 'community/members'
MEMBER_DIRECTORY_ID = 'members'
MEMBER_PORTAL_TYPE = 'cloudspring.sfmembers.member'
PUBLISH_ACTION = 'publish'
logger = logging.getLogger('Create Member Area')

class CreateMemberArea(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.wftool = getToolByName(self.context, 'portal_workflow')
        self.normalizer = getUtility(IIDNormalizer)

    def publish(self, item):
        # publish and reindex
        try:
            self.wftool.doActionFor(item, PUBLISH_ACTION)
        except:
            logger.info("Failed to publish %s" % item.Title)
            pass
        item.reindexObject(idxs=['Title'])


    def getDirectoryFolder(self, dir, id):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        member_dir_path = MEMBER_DIRECTORY.split("/")
        cur_dir = portal.unrestrictedTraverse('/')
        for dir in member_dir_path:
            try:
                cur_dir = cur_dir.unrestrictedTravers(dir)
            except KeyError:
               # folder doesn't exist yet, so create it.
               cur_dir.invokeFactory("Folder", dir)
               cur_dir = getattr(cur_dir, dir)
               cur_dir.setTitle(cur_dir.id.capwords())
               cur_dir.reindexObject(idxs=['Title'])
            publish(cur_dir)

        member_dir = cur_dir

        # look for the member's folder
        try:
            directory = member_dir.unrestrictedTraverse(id)
        except:
             # Doesn't exist.  Create it!
             member_dir.invokeFactory("Folder", id)

        directory = getattr(member_dir, id)

        return directory

    def findOrCreateProfileById(self, name, id):
        res = self.catalog.searchResults(id = id)
        if res:
            # update existing profile
            profile = res[0].getObject()
            logger.info('Updating %s' % '/'.join(profile.getPhysicalPath()))
            return profile
        else:
            # didn't match ID: create new profile
            #name = safe_unicode(name)
            #profile_id = self.normalizer.normalize(name)
            directory = self.getDirectoryFolder(MEMBER_DIRECTORY, id)
            dir = getattr(directory, id)

            # Change the title to the members fullname.
            dir.setTitle(name)

            # publish and reindex
            publish(dir)

            # look for the member's blog folder
            try:
                blog_folder = dir.unrestrictedTraverse('blog')
            except:
                dir.invokeFactory("Folder", 'blog')
            blog_folder = getattr(dir, 'blog')

            # Change ownership and give local roles to member folder
            acl_users = getToolByName(self, "acl_users")
            user = acl_users.getUserById(id)
            blog_folder.changeOwnership(user)
            blog_folder.__ac_local_roles__ = None
            blog_folder.manage_setLocalRoles(id, ['Owner'])

            blog_field = blog_folder.getField('blog_folder')
            if blog_field:
                blog_field.set(blog_folder, True)

            # Hide the blog folder from navigation.
            blog_folder.setExcludeFromNav(True)

            # publish and reindex
            publish(blog_folder)

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
            publish(blog_collection)

            # set the default page for the home folder to the collection
            dir.setDefaultPage("blog-collection")

            # get the member profile object, if it exists.
            try:
                profile = getattr(dir, "profile")
            except:
                # The profile doesn't exists, so create it.
                profile_id = dir.invokeFactory(MEMBER_PORTAL_TYPE, "profile")
                profile = getattr(dir, profile_id)

            profile_title = "%s's profile" % name
            profile.setTitle(profile_title)
            # Hide the profile from navigation.
            profile.setExcludeFromNav(True)
            # Change ownership and give local roles to member profile
            profile.changeOwnership(user)
            profile.__ac_local_roles__ = None
            profile.manage_setLocalRoles(id, ['Owner'])

            logger.info('Creating %s' % '/'.join(profile.getPhysicalPath()))

        return profile

    def updateProfile(self, profile, data):
        logger.info("Updating " + data.Name)
        profile.id = data.id
        profile.name = data.Name
        profile.firstName = data.FirstName
        profile.lastName = data.LastName
        profile.email = data.Email
        profile.role = data.role

        # publish and reindex
        publish(profile)

    def __call__(self, member=member):
        """ Creates a member area including blog and profile
            for a plone memember 
        """

        profile = self.findOrCreateProfileById(name = member.Name, id = member.id)
        logger.info("profile.Title: " + profile.title)
        self.updateProfile(profile, data)
 
