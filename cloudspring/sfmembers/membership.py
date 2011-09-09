from Products.CMFCore.utils import getToolByName

def getHome(context, id=None):
    if id is None:
        # If no id is passed, get the currently
        # authenticated user.
        mt = getToolByName(context, 'portal_membership')
        member = mt.getAuthenticatedMember()
        id = member.getUserName()
    # Find the users home folder in the catalog.
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog.searchResults(
                    {'portal_type': 'Folder', 
                     'path': {'query': '/Plone/members', 
                              'depth': 2},
                     'id': id})
    for brain in results:
        return brain

def getBlog(context, id=None):
    portal_url = getToolByName(context, "portal_url")
    blog = portal_url.unrestrictedTraverse(getHome(context, id).getPath())
    return blog

def getHomeUrl(self, id=None, verifyPermission=0):
    home = getHome(self.context, id)
    if home is not None:
        return home.getURL()

def getHomePath(context, id=None):
    home = getHome(context, id)
    if home:
        return home.getPath()


