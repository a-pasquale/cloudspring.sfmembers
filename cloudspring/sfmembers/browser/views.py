from Products.Five.browser import BrowserView
from zope.interface import implements, Interface

from Products.CMFCore.utils import getToolByName
from cloudspring.sfmembers.browser.interfaces import IMemberSummaryView


class MemberSummaryView(BrowserView):
    """ 
    List members in the folder.
    """

    implements(IMemberSummaryView)

    def __call__(self):
        """ Render the content item listing.
        """

        # How many items is one one page
        limit = 30

        # Read the first index of the selected batch parameter as 
        # HTTP GET request query parameter
        start = self.request.get("b_start", 0)

        contentFilter = {}
        contentFilter['portal_type'] = 'Folder'
        contentFilter['sort_on'] = 'getObjPositionInParent'
        contentFilter['sort_order'] = 'ascending'
        
        cur_path = '/'.join(self.context.getPhysicalPath())
        path = {}

        path['query'] = cur_path
        path['depth'] = 1
        contentFilter['path'] = path

        self.contents = self.context.portal_catalog.queryCatalog(contentFilter, show_all=1, show_inactive=False)

        self.contents = [b.getObject() for b in self.contents]

        batch = True
        if batch:
            from Products.CMFPlone import Batch
            b_start = self.context.REQUEST.get('b_start', 0)
            self.contents = Batch(self.contents, limit, int(b_start), orphan=0)

        # Return the rendered template with content listing info filled in
        return self.index()

