import unittest
from cloudspring.sfmembers.tests.base import IntegrationTestCase

# from example.dexteritypage.interfaces import ILayer
# 
# from zope.component import getMultiAdapter, queryMultiAdapter, getUtility
# 
# from example.dexteritypage.interfaces import IArticle, IRelatable


class TestContent(IntegrationTestCase):
    
    def test_creation(self):
        # Will raise an exception if we can't add this content
        self.folder.invokeFactory('cloudspring.sfmembers.member', 'member')
        self.folder.invokeFactory('cloudspring.sfmembers.organization', 'organization')
    
    def test_member_properties(self):
         self.folder.invokeFactory('cloudspring.sfmembers.member', 'm')
         m = getattr(self.folder, 'm')
         m.title = u"Title"
         m.description = u"Description"
         m.bio = u"Some text"
         
         self.assertEquals(u"Title", m.Title())
         self.assertEquals(u"Description", m.Description())
         self.assertEquals(u"Some text", m.bio)

    def test_organization_properties(self):
         self.folder.invokeFactory('cloudspring.sfmembers.organization', 'o')
         o = getattr(self.folder, 'o')
         o.title = u"Title"
         o.description = u"Description"
         o.detailedDescription = u"Some text"
         
         self.assertEquals(u"Title", o.Title())
         self.assertEquals(u"Description", o.Description())
         self.assertEquals(u"Some text", o.detailedDescription())
    
    # def test_news_item_schema(self):
    #     self.folder.invokeFactory('News Item', 'n1')
    #     n1 = getattr(self.folder, 'n1')
    #     field = n1.getField('relatedArticles')
    #     self.failIf(field is None)
    #     
    #     
    #     
    #     
    # def test_article_suggestion_form(self):        
    #     self.folder.invokeFactory('Article', 'a1')
    #     a1 = getattr(self.folder, 'a1')
    #     
    #     view = getMultiAdapter((a1, self.app.REQUEST), name=u'suggest-idea')
    #     self.failUnless(view)    
    # 
    #     self.failUnless(IArticle.providedBy(a1))
    #     self.failUnless(IRelatable.providedBy(a1))
    #     # import pdb ; pdb.set_trace( )
    #     # a1.restrictedTraverse('@@suggest-idea', default=None)

        
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestContent))
    return suite

