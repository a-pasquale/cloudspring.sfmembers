from five import grok
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from cloudspring.sfmembers import _

class IReflection(form.Schema):
    """  A reflection
    """

    text = RichText(
            title=_(u"Text"),
            )
    

class blog_item_view(grok.View):
    grok.context(IReflection)
    grok.require('zope2.View')



