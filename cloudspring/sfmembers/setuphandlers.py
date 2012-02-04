from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFCore.WorkflowCore import WorkflowException

PUBLISH_ACTION = "publish"

def deletePloneFolders(p):
    """Delete the standard Plone stuff that we don't need
    """
    # Delete standard Plone stuff..
    existing = p.objectIds()
    #itemsToDelete = ['Members', 'news', 'events']
    itemsToDelete = []
    for item in itemsToDelete:
        if item in existing:
            p.manage_delObjects(item)

def createFolderStructure(portal):
    """Define which objects we want to create in the site.
    """

    members_children = [
        {    'id': 'members-collection',
             'title': 'Members',
             'description': '',
             'type': 'Topic',
             'layout': 'member_summary_view',
             'criteria': [ 
                 {    'type': 'path',
                      'value': '..', 
                      },
                 {    'type': 'item_type',
                      'value': 'Folder',
                      },
                 ],
             'default': True,
             'excludeFromNav': False,
             },
        ]
    community_children = [
        {   'id': 'members', 
            'title': 'Members',
            'description': '',
            'type': 'Folder',
            'excludeFromNav': False,
            'criteria': [],
            #'children': members_children,
            },
        ]
    top_folders = [
        {   'id': 'community', 
            'title': 'Community',
            'description': '',
            'type': 'Folder',
            'criterion': [],
            'excludeFromNav': False,
            'children': community_children,
            },
        ]
    createObjects(portal, parent=portal, children=top_folders)

def createObjects(portal, parent, children):
    """This will create new objects, or modify existing ones if id's and type
    match.
    """
    parent.plone_log("Creating %s in %s" % (children, parent))
    existing = parent.objectIds()
    parent.plone_log("Existing ids: %s" % existing)
    for new_object in children:
        if new_object['id'] in existing:
            parent.plone_log("%s exists, skipping" % new_object['id'])
        else:
            _createObjectByType(new_object['type'], parent, \
                id=new_object['id'], title=new_object['title'], \
                description=new_object['description'])
        parent.plone_log("Now to modify the new_object...")
        obj = parent.get(new_object['id'], None)
        if obj is None:
            parent.plone_log("can't get new_object %s to modify it!" % new_object['id'])
        else:
            if obj.Type() != new_object['type']:
                if obj.Type() == 'Collection':
                    for criterion in new_object['criteria']:
                        if criterion['type'] == 'path':
                            path = criterion['value']
                            try: 
                                path_criteria = obj.addCriterion('path', 'ATRelativePathCriterion')
                                path_criteria.setRelativePath(path)
                            except:
                                pass
                        if criterion['type'] == 'item_type':
                            item_type = criterion['value']
                            try: 
                                type_criteria = obj.addCriterion('Type','ATPortalTypeCriterion')
                                type_criteria.setValue(item_type)
                            except:
                                pass

                    obj.setLayout(new_object['layout'])
                    if new_object['default']:
                        parent.setDefaultPage(new_object['id'])
                    # Publish it
                    wftool = getToolByName(portal, 'portal_workflow')
                    try:
                        wftool.doActionFor(obj, PUBLISH_ACTION)
                    except WorkflowException:
                        pass

                    if new_object['excludeFromNav']:
                        obj.setExcludeFromNav(True)

                    obj.reindexObject()
                    
                parent.plone_log("types don't match!")
            else:
                parent.plone_log("object type is %s " % new_object['type'])
                #obj.setLayout(new_object['layout'])

                # Publish it
                wftool = getToolByName(portal, 'portal_workflow')
                try:
                    wftool.doActionFor(obj, PUBLISH_ACTION)
                except WorkflowException:
                    pass

                if new_object['excludeFromNav']:
                    obj.setExcludeFromNav(True)

                obj.reindexObject()
                children = new_object.get('children',[])
                if len(children) > 0:
                    createObjects(portal, obj, children)

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    portal = context.getSite()

    if context.readDataFile('cloudspring.sfmembers.marker.txt') is None:
        return

    # Add additional setup code here
    deletePloneFolders(portal)
    createFolderStructure(portal)
    # These remove any old indices that might be around from 
    # previous versions of cloudspring.sfmembers
    smart_folder_tool = getToolByName(context, 'portal_atct')
    smart_folder_tool.removeIndex("ProjectField")
    smart_folder_tool.removeMetadata("ProjectField")
    smart_folder_tool.removeIndex("projects")
    smart_folder_tool.removeMetadata("projects")
