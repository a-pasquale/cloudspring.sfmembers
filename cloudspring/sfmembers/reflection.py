from five import grok
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from zope.interface import implements
from plone.behavior.interfaces import IBehaviorAssignable
from collective.gtags.behaviors import ITags
from zope.component import adapts
from zope.component import provideAdapter
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
    

#class Reflection(object):
#    implements(IBehaviorAssignable)
#    adapts(IReflection)
#
#    enabled = [ITags]
#
#    def __init__(self, context):
#        self.context = context
#        
#    def supports(self, behavior_interface):
#        return behavior_interface in self.enabled
#    
#    def enumerate_behaviors(self):
#        for e in self.enabled:
#            yield queryUtility(IBehavior, name=e.__identifier__)
#
#provideAdapter(ReflectionAssignable)

class blog_item_view(grok.View):
    grok.context(IReflection)
    grok.require('zope2.View')



