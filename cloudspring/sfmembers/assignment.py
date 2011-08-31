from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from five import grok

class possibleAssignmentsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            path={'query': '/Plone/assignments/assignments','depth': 1},
            review_state='published',
            portal_type='Event',
            sort_on='sortable_title'
            )
        terms = []
        if results is not None:
            for brain in results:
                terms.append(SimpleVocabulary.createTerm(brain.Title))
        return SimpleVocabulary(terms)

grok.global_utility(possibleAssignmentsVocabulary,
        name=u"cloudspring.sfmembers.possibleAssignments")
