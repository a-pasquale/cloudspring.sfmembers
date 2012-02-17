from Products.CMFCore.utils import getToolByName
from settings import MEMBER_DIR_PATH

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
                     'path': {'query': "Plone%s" % MEMBER_DIR_PATH, 
                              'depth': 2},
                     'id': id})
    for brain in results:
        return brain

def getBlog(context, id=None):
    d = getToolByName(context, "portal_url")
    home = getHome(context, id)
    if home:
        member_dir_path = MEMBER_DIR_PATH.split("/")
        for dir in member_dir_path:
            d = d.unrestrictedTraverse(dir)
        return d.unrestrictedTraverse(home.getPath())

def getHomeUrl(context, id=None, verifyPermission=0):
    home = getHome(context, id)
    if home is not None:
        return home.getURL()

def getHomePath(context, id=None):
    home = getHome(context, id)
    if home:
        return home.getPath()


