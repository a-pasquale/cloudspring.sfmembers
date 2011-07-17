from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
import re

START_RE = re.compile('<h1[^<>]+documentFirstHeading[^<>]+>') # Standard plone header
END_RE = re.compile('</h1>')

class DefaultItemView(BrowserView):
    """
    The default blog item view
    """
    
    template = ViewPageTemplateFile("./default_item.pt")
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        html = self.template()
        tag = START_RE.search(html)
        if not tag:
            return html
        startpos = tag.end()
        endpos = END_RE.search(html, startpos).start()

        portal_properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        use_view = site_properties.getProperty('typesUseViewActionInListings')
        if self.context.portal_type in use_view:
            postfix = '/view'
        else:
            postfix = ''

        result = (html[:startpos],
                  '<a href="',
                  self.context.absolute_url(),
                  postfix,
                  '">',
                  html[startpos:endpos],
                  '</a>',
                  html[endpos:])
        return ''.join(result)
