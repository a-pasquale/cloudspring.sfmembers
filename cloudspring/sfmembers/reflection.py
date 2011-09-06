from five import grok
from zope import schema
from plone.directives import form, dexterity
from zope.interface import implements
from plone.app.textfield import RichText
from plone.dexterity.content import Item
from rwproperty import getproperty, setproperty
from cloudspring.sfmembers import _

class IReflection(form.Schema):
    """  A reflection
    """

    title = schema.TextLine(
            title=_(u"Title"),
            )

    text = RichText(
            title=_(u"Text"),
            )
    
    assignment = schema.Choice(
            title=_(u"Assignment:"),
            values=[_(u'Public Narrative'), _(u'Political Autobiography'),],
            #source="cloudspring.sfmembers.possibleAssignments",
            required=False,
            )

    projectField = schema.List(
            title=_(u"Projects:"),
            value_type=schema.Choice(
                values=[
                    _(u'Syracuse'), 
                    _(u'Rutgers Future Scholars'),
                    _(u'Innovative Lawyering'), 
                    _(u'Higher Education and Immigration'), 
                    _(u'College Initiative')],
                ),
            required=False,
            )

    #projects = schema.Set(
    #        title=_(u"Projects:"),
    #        value_type=schema.Choice(
    #            title=_(u"Projects"),
    #            vocabulary="cloudspring.sfmembers.possibleProjects",
    #            ),
    #        required=False,
    #        )

class Refliection(Item):
    implements(IReflection)

    def __init__(self, context):
        self.context = context

    @setproperty
    def Title(self):
        return self.title

    @getproperty
    def Title(self):
        return self.title

    @getproperty
    def absolute_url(self):
        return self.absolute_url()


class blog_item_view(grok.View):
    grok.context(IReflection)
    grok.require('zope2.View')



