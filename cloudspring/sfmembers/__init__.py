  # -*- extra stuff goes here -*- 
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("cloudspring.sfmembers")

from AccessControl import allow_module

allow_module('cloudspring.sfmembers.notifyMemberAreaCreated')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
