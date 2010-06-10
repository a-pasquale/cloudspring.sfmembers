import unittest
from cloudspring.sfmembers.tests.base import IntegrationTestCase
from cloudspring.sfmembers.member import MemberOrgs 
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
         # Create a member object.
         self.folder.invokeFactory('cloudspring.sfmembers.member', 'm')

         # Test the basic properties of a member object.
         m = getattr(self.folder, 'm')
         m.title = u"Title"
         m.description = u"Description"
         m.bio = u"Some text"

         self.assertEquals(u"Title", m.Title())
         self.assertEquals(u"Description", m.Description())
         self.assertEquals(u"Some text", m.bio)

         # Test the affiated organizations object.
         # member.relatedOrganizations is a list of dict objects. 
         from cloudspring.sfmembers.member import MemberOrgs
         org1 = dict({"orgId": u"cloudspring", 
                      "orgName": u"Cloudspring", 
                      "role": u"developer"})
         org2 = dict({"orgId": u"elytra", 
                      "orgName": u"Elytra",
                      "role": u"president"})

         relOrg1 = MemberOrgs(org1)
         relOrg2 = MemberOrgs(org2)
         m.relatedOrganizations = [org1, org2]
         
         orgs = m.relatedOrganizations
         self.assertEquals(u"cloudspring", orgs[0]["orgId"])
         self.assertEquals(u"president",orgs[1]["role"])
         

    def test_organization_properties(self):
         # Create a organization object.
         self.folder.invokeFactory('cloudspring.sfmembers.organization', 'o')

         # Test the basic organization properties.
         o = getattr(self.folder, 'o')
         o.title = u"Title"
         o.description = u"Description"
         o.detailedDescription = u"Some text"
         
         self.assertEquals(u"Title", o.Title())
         self.assertEquals(u"Description", o.Description())
         self.assertEquals(u"Some text", o.detailedDescription)
    
         # Test the affiliated members object.
         # organization.relatedMembers is a list of dict objects. 
         from cloudspring.sfmembers.organization import OrgMembers
         member1 = dict({"memberId": u"apasquale", 
                      "memberName": u"Andrew Pasquale", 
                      "role": u"developer"})
         member2 = dict({"memberId": u"khomstead", 
                      "memberName": u"Kyle Homstead",
                      "role": u"president"})

         relMember1 = OrgMembers(member1)
         relMember2 = OrgMembers(member2)
         o.relatedMembers = [member1, member2]
         
         members = o.relatedMembers
         self.assertEquals(u"apasquale", members[0]["memberId"])
         self.assertEquals(u"Kyle Homstead", members[1]["memberName"])
    # def test_news_item_schema(self):
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

