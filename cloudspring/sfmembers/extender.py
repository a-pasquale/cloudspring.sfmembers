from archetypes.schemaextender.field import ExtensionField
from zope.component import adapts
from zope.interface import implements
from zope import schema
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import LinesField, MultiSelectionWidget
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.Archetypes.public import DisplayList
from cloudspring.sfmembers import _

class BlogTypeField(ExtensionField, LinesField):
    pass

class BlogExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)


    fields = [ 
        BlogTypeField(name='BlogTypeField',
                  vocabulary=DisplayList((('News2','News2'), ('Astronomy','Astronomy'), ('Biology','Biology'), ('Chemistry','Chemistry'), ('Materials','Materials'), ('Physics','Physics'), ('Personal','Personal'))),
                  widget=MultiSelectionWidget(
                      label=_(u'Blog type:'),
                      format='checkbox'
                  ),
        ),
    ]
 
    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

