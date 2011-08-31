from five import grok
from zope.interface import Interface
from Acquisition import aq_inner
from Products.CMFCore.utils  import getToolByName
from plone.namedfile.file import NamedImage
from plone.namedfile.scaling import ImageScaling
import membership
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

        member_folder = membership.getBlog(self.context)
 
        # A dictionary of items submitted in a POST request
        form = self.request.form
        self.update_value = form['update_value']

        member_props = {}

        if "name" in form:
            member_folder.Title = self.update_value
            member_folder.profile.name = self.update_value
            member_folder.profile.Title = "%s's profile" % self.update_value
            blog_title = "%s's Blog" % self.update_value
            blog_collection = getattr(member_folder, "blog-collection")
            blog_collection.Title = blog_title
            member_props.update({ "fullname" : self.update_value })

        if "email" in form:
            member_folder.profile.email = self.update_value
            member_props.update({ "email" : self.update_value })

        if "website" in form:
            member_folder.profile.website = self.update_value

        if "picture" in form:
            self.update_value.seek(0)
            image = self.update_value.read()
            member_folder.profile.picture = NamedImage(data=image, filename='picture')
            #member_folder.profile.scaling.scale('picture', scale='mini')

        # Update the plone member object to be thorough.
        mt = getToolByName(self.context, 'portal_membership')
        if mt.isAnonymousUser(): # the user has not logged in
            return None
        else:
            member = mt.getAuthenticatedMember()

        member.setMemberProperties(mapping=member_props)
