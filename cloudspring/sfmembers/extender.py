from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from zope import schema
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import StringField, SelectionWidget
from Products.ATContentTypes.content.newsitem import ATNewsItem
from cloudspring.sfmembers import _
class BlogTypeField(ExtensionField, StringField):
    pass

class BlogExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)


    fields = [ 
        BlogTypeField(name='BlogTypeField',
                  vocabulary=[_(u'Pre-class reflection'), _(u'Post-class reflection'), _(u'Seminar feed'), _(u'Personal blog')],
                  widget=SelectionWidget(
                      label=_(u'Blog type:'),
                      format='radio'
                  ),
        ),
    ]
 
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

