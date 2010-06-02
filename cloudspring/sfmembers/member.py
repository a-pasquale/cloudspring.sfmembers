from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from cloudspring.sfmembers import _

class IMember(form.Schema):
    """A Salesforce Contact representing a member in Plone.
    """
    
    title = schema.TextLine(
            title=_(u"Name"),
        )
    
    description = schema.Text(
            title=_(u"A short summary"),
        )
    
    form.primary('bio')
    bio = RichText(
            title=_(u"Bio"),
            required=False
        )
    form.primary('picture')
    picture = NamedImage(
            title=_(u"Picture"),
            description=_(u"Please upload an image"),
            required=False,
        )

class View(grok.View):
    grok.context(IMember)
    grok.require('zope2.View')

    def published_content(self):
        """Return a catalog search result of members content.
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(Creator=context.title,
                       sort_order='sortable_title')
