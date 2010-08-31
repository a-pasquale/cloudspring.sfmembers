from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager
    
class IActionbarPanel(IViewletManager):
    """A viewlet manager that sits at the bottom of the page
    """

class IActionbarPanelLayer(Interface):
    """Marker Interface for a custom BrowserLayer
    """
