from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from cloudspring.sfmembers import _

class IOrganization(form.Schema):
    """A Salesforce Account representing a organization in Plone.
    """
    
    title = schema.TextLine(
            title=_(u"Organization Name"),
        )
    
    description = schema.Text(
            title=_(u"A short description"),
        )
    
    form.primary('detailedDescription')
    detailedDescription = RichText(
            title=_(u"Detailed description of the organization"),
            required=False
        )

class View(grok.View):
    grok.context(IOrganization)
    grok.require('zope2.View')

    def published_content(self):
        """Return a catalog search result of members content.
        """
        
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        return catalog(Creator=context.title,
                       sort_order='sortable_title')
