from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface
from zope import schema

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer bound to a Skin
       Selection in portal_skins.
    """

class IMemberSummaryView(Interface):
    """ Allowed template variables exposed from the view.
    """

    # Item list as iterable Products.CMFPlone.PloneBatch.Batch object
    contents = schema.Object(Interface)
