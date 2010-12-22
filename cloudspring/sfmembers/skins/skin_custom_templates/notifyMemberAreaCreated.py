## Script (Python) "notifyMemberAreaCreated"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Modify new member area
##

import logging
from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.createMemberArea import createMemberArea

logger=logging.getLogger('Notify Member Area Created')
logger.info('starting notifyMemberAreaCreated , context is %s' % context)

portal_membership = getToolByName(context,'portal_membership')
member = portal_membership.getAuthenticatedMember()
id = member.getUserName()
name = member.getProperty("fullname")
email = member.getProperty("email")

firstName = ''
lastName = ''
role = ''

request = context.REQUEST

logger.info("Member name: %s, id: %s" % (name, id))

createMemberArea(context, name, firstName, lastName, id, email, role)

logger.info('ending notifyMemberAreaCreated')

