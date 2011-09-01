from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from five import grok

class possibleProjectsVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            path={'query': '/Plone/projects','depth': 1},
            review_state='published',
            sort_on='sortable_title'
            )
        terms = []
        if results is not None:
            for brain in results:
                terms.append(SimpleVocabulary.createTerm(brain.Title))
        return SimpleVocabulary(terms)

grok.global_utility(possibleProjectsVocabulary,
        name=u"cloudspring.sfmembers.possibleProjects")
