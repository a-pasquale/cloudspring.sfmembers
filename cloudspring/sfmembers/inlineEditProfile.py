from five import grok
from zope.interface import Interface
from Acquisition import aq_inner
from Products.CMFCore.utils  import getToolByName
import logging
from cloudspring.sfmembers import _

class inline_edit_view(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')

    def render(self):
        """No-op to keep grok.View happy
        """
        return self.update_value

    def update(self):
        logger = logging.getLogger('inline edit')
        self.errors = {}

        mt = getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser(): # the user has not logged in
            return None
        else:
            member = mt.getAuthenticatedMember()
            username = member.getUserName()

        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        member_folder = portal.community.members[username]
 
        # A dictionary of items submitted in a POST request
        form = self.request.form
        self.update_value = form['update_value']

        if "name" in form:
            member_folder.profile.name = self.update_value
            blog_title = "%s's Blog" % self.update_value
            blog_collection = getattr(member_folder, "blog-collection")
            blog_collection.setTitle(blog_title)

        if "email" in form:
            member_folder.profile.email = self.update_value
