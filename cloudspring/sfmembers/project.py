from persistent import Persistent 
from OFS.SimpleItem import SimpleItem

from zope.interface import implements, Interface
from zope.component import adapts
from zope.formlib import form
from zope import schema
from zope.app.component.hooks import getSite

from zope.component.interfaces import IObjectEvent

from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 

from Acquisition import aq_inner

from Products.CMFPlone import PloneMessageFactory as _

class IProjectCondition(Interface):
    """Interface for the configurable aspects of the condition.
    
    This is also used to create add and edit forms, below.
    """
    
    projects = schema.Tuple(title=_(u"Project"),
                            description=_(u"The project to check for."),
                            required=True,
                            value_type=schema.TextLine(title=_(u"Project")))

class ProjectCondition(SimpleItem):
    """The actual persistent implementation of the condition element.
    
    Note that we must mix in SimpleItem to keep Zope 2 security happy.
    """
    implements(IProjectCondition, IRuleElementData)
    
    projects = []
    element = "cloudspring.sfmembers.Project"
    
    @property
    def summary(self):
        return _(u"Project contains: ${names}", mapping=dict(names=", ".join(self.projects)))

class ProjectConditionExecutor(object):
    """The executor for this condition.
    
    This is registered as an adapter in configure.zcml
    """
    implements(IExecutable)
    adapts(Interface, IProjectCondition, IObjectEvent)
         
    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        context = aq_inner(self.event.object)
        try:
            projects = context.getField('ProjectField').getAccessor(context)()
        except (AttributeError, TypeError,):
            # The object doesn't have a ProjectField method
            return False
        return (projects == ''.join(self.element.projects))

class ProjectAddForm(AddForm):
    """An add form for portal type conditions.
    """
    form_fields = form.FormFields(IProjectCondition)
    label = _(u"Add Project Condition")
    description = _(u"A condition that makes the rule apply only to content related to certain projects.")
    form_name = _(u"Configure element")
    
    def create(self, data):
        c = ProjectCondition()
        form.applyChanges(c, self.form_fields, data)
        return c

class ProjectEditForm(EditForm):
    """An edit form for portal type conditions
    """
    form_fields = form.FormFields(IProjectCondition)
    label = _(u"Edit Project Condition")
    description = _(u"A condition that makes the rule apply only to content related to certain projects.")
    form_name = _(u"Configure element")
