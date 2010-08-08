from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName

class ProfileViewlet(ViewletBase):
    render = ViewPageTemplateFile('profile.pt')

    def update(self):
        sf_id = self.context.getId()
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(id=sf_id)

        for member in results:
            self.name = member.Title
            self.url = "%s/profile" % member.getURL()        
