from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _

class IProfilePortlet(IPortletDataProvider):
    """Portlet to display profile information.
    """

class IQuickPostPortlet(IPortletDataProvider):
    """Portlet to allow members to make quick posts.
    """
