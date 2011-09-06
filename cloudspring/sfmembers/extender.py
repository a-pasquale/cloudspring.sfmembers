from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from zope import schema
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import StringField, SelectionWidget, MultiSelectionWidget, StringWidget, LinesField
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.Archetypes.public import DisplayList
from cloudspring.sfmembers import _

class assignment(ExtensionField, StringField):
    pass

class ProjectField(ExtensionField, LinesField):
    pass

class BlogExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)


    fields = [ 

        assignment(name=_(u"Assignment"),
                   title=_(u"Assignment"),
                   vocabulary=[_(u'Select an assignment'),_(u'Public Narrative'), _(u'Political Autobiography'),],
                   required=False,
                   widget=SelectionWidget(
                       format='select'
                   ),
        ),

        ProjectField(
            name=_(u"ProjectField"),
            vocabulary=[_(u'Syracuse'), _(u'Rutgers Future Scholars'), _(u'Innovative Lawyering'), _(u'Higher Education and Immigration'), _(u'College Initiative')],
            widget=MultiSelectionWidget(
                label=_(u"Select a project:"),
                format='select',
            ),
        ),
    ]
 
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

