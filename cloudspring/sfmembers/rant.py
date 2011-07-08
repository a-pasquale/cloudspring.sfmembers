from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText

from cloudspring.sfmembers import _

class IRant(form.Schema):
    """  A rant
    """

    title = schema.TextLine(
            title=_(u"Title"),
            )

    text = RichText(
            title=_(u"Text"),
            )
    
