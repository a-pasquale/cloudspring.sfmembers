from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from zope import schema
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import StringField, SelectionWidget, StringWidget
from Products.ATContentTypes.content.newsitem import ATNewsItem
from cloudspring.sfmembers import _


class BlogTypeField(ExtensionField, StringField):
    pass

class AssignmentNumberField(ExtensionField, StringField):
    pass

class ProjectField(ExtensionField, StringField):
    pass

class BlogExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)


    fields = [ 
        BlogTypeField(name='BlogTypeField',
                  vocabulary=[_(u'Assignment'),_(u'Pre-class reflection'), _(u'Post-class reflection'), _(u'Project'), _(u'Seminar feed'), _(u'Personal blog')],
                  widget=SelectionWidget(
                      label=_(u'Blog type:'),
                      format='radio'
                  ),
        ),
        AssignmentNumberField(
            name=_(u"AssignmentNumberField"),
            widget=StringWidget(
                label=_(u"Assignment number:"),            
                description=_(u"Enter the relevant class number."),
            ),
        ),

        ProjectField(
            name=_(u"ProjectField"),
            vocabulary=[_(u'Syracuse'), _(u'Rutgers Future Scholars'), _(u'Innovative Lawyering'), _(u'Higher Education and Immigration'), _(u'College Initiative')],
            widget=SelectionWidget(
                label=_(u"Select a project:"),            
                format='radio',
            ),
        ),
    ]
 
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

