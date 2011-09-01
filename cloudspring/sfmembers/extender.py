from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from zope import schema
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import StringField, SelectionWidget, MultiSelectionWidget, StringWidget
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.Archetypes.public import DisplayList
from cloudspring.sfmembers import _

class assignment(ExtensionField, StringField):
    pass

class ProjectField(ExtensionField, StringField):
    pass

class BlogExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)


    fields = [ 

        assignment(name=_(u"Assignment"),
                   title=_(u"Assignment"),
                   vocabulary=[_(u'Assignment 1'), _(u'Assignment 2'),
                       _(u'Assignment 3'), _(u'Assignment 4')],
                   required=False,
                   widget=SelectionWidget(
                       format='radio'
                   ),
        ),

        ProjectField(
            name=_(u"ProjectField"),
            vocabulary=[_(u'Syracuse'), _(u'Rutgers Future Scholars'), _(u'Innovative Lawyering'), _(u'Higher Education and Immigration'), _(u'College Initiative')],
            widget=MultiSelectionWidget(
                label=_(u"Select a project:"),            
                format='checkbox',
            ),
        ),
    ]
 
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

