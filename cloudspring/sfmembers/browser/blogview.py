import logging
from time import time
from Acquisition import aq_inner
from zope.component import getMultiAdapter
from zope.interface import implements

from Products.ATContentTypes.interface import (IATTopic, IATFolder, IATBTreeFolder,
                                                IATNewsItem, IATEvent, IATLink, IATImage,
                                                IATFile)
from Products.CMFPlone import Batch
from Products.Five import BrowserView

from plone.memoize import view, ram, volatile

from collective.blogging.interfaces import IEntryMarker, IBloggingView
from collective.blogging import _

logger = logging.getLogger('collective.blogging')


def _filter_cachekey(method, self):
    """ Time and path based cache """
    path = '/'.join(self.context.getPhysicalPath())
    interval = 60
    int_fld = self.context.getField('filter_cache')
    if int_fld:
        interval = int_fld.get(self.context)
        if interval == 0:
            # Avoid ZeroDivisionError by raising a different error
            # that will be caught by plone.memoize
            raise volatile.DontCache
    return hash((path, time() // (60 * interval)))


class BlogView(BrowserView):
    """ A blog browser view """

    implements(IBloggingView)
    
    def __init__(self, context, request):
        super(BlogView, self).__init__(context, request)
        self.context = context
        self.request = request

    @property
    def tools(self):
        return getMultiAdapter((self.context, self.request), name=u'plone_tools')

    @property
    def portal_state(self):
        return getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

    def getFieldValue(self, name, obj=None):
        if obj is None:
            obj = self.context

        field = obj.getField(name)
        if field:
            return field.get(obj)
        return None

    @view.memoize
    def contents(self):
        brains = []
        criteria = {}

        # filter criteria
        subject = self.request.get('Subject', None)
        if subject and subject != ['']:
            criteria['Subject'] = subject

        year = self.request.get('publish_year', None)
        if year:
            criteria['publish_year'] = int(year)

        month = self.request.get('publish_month', None)
        if month:
            # Note: months are indexed as for example '03'
            criteria['publish_month'] = month

        if self.is_topic:
            brains = self.context.queryCatalog(criteria)
        else:
            criteria['object_provides'] = IEntryMarker.__identifier__
            criteria['path'] = '/'.join(self.context.getPhysicalPath())
            criteria['sort_on'] = 'effective'
            criteria['sort_order'] = 'reverse'
            brains = self.tools.catalog()(criteria)
        return brains

    def batch(self):
        b_start = self.request.get('b_start', 0)
        return Batch(self.contents(), self.batch_size, int(b_start), orphan=0)

    @property
    def count(self):
        return len(self.contents())

    @property
    def is_folder(self):
        return IATFolder.providedBy(self.context) or \
            IATBTreeFolder.providedBy(self.context)

    @property
    def is_topic(self):
        return IATTopic.providedBy(self.context)

    @property
    def site_props(self):
        pprops = self.tools.properties()
        return getattr(pprops, 'site_properties')

    @property
    def getText(self):
        text_field = self.context.getField('text')
        if text_field:
            return text_field.get(self.context)
        return self.context.getField('blog_text').get(self.context)

    @property
    def show_about(self):
        return not self.portal_state.anonymous() or \
            self.site_props.getProperty('allowAnonymousViewAbout', False)

    @property
    def show_toolbar(self):
        field = self.context.getField('enable_toolbar')
        if field:
            return field.get(self.context)
        return True

    @property
    def show_count(self):
        field = self.context.getField('enable_count')
        if field:
            return field.get(self.context)
        return True

    @property
    def show_body(self):
        field = self.context.getField('enable_full')
        if field:
            return field.get(self.context)
        return False

    @property
    def batch_size(self):
        field = self.context.getField('batch_size')
        if field:
            return field.get(self.context)
        return 10

    @ram.cache(_filter_cachekey)
    def filter_info(self):
        logger.info('Caching filter info')
        subject = self.request.get('Subject')
        year    = self.request.get('publish_year')
        month   = self.request.get('publish_month')

        subjects = set()
        years = set()
        months = set()
        for brain in self.contents():
            for s in brain.Subject:
                subjects.add(s)
            if brain.publish_year:
                years.add(brain.publish_year)
            if brain.publish_month:
                months.add(brain.publish_month)
        subjects = list(subjects)
        years = list(years)
        months = list(months)

        subjects.sort()
        years.sort()
        months.sort()

        return [
            {
                'id': 'Subject:list',
                'title': _(u'select_category_option', default=u'-- Category --'),
                'options': subjects,
                'selected': subject and subject != [''] and subject[0] or None
            },
            {
                'id': 'publish_year',
                'title': _(u'select_year_option', default=u'-- Year --'),
                'options': years,
                'selected': year and int(year) or None
            },
            {
                'id': 'publish_month',
                'title': _(u'select_month_option', default=u'-- Month --'),
                'options': months,
                'selected': month and int(month) or None
            }
        ]

    # Image related
    def is_image(self, obj):
        return IATImage.providedBy(obj)

    def image_size(self, obj):
        context = aq_inner(obj)
        return context.getObjSize(context)

    # News Item related
    def is_newsitem(self, obj):
        return IATNewsItem.providedBy(obj)

    # Event related
    def is_event(self, obj):
        return IATEvent.providedBy(obj)

    # File related
    def is_file(self, obj):
        return IATFile.providedBy(obj)

    def file_info(self, obj):
        context = aq_inner(obj)
        field = context.getField('file')
        fl = field.get(context)
        size = fl.get_size() or fl and len(fl) or 0
        return {
            'icon': fl.getBestIcon() or None,
            'filename': fl.filename or None,
            'content_type': context.lookupMime(field.getContentType(context)),
            'size': '%sKb' % (size / 1024)
        }

    # Link related
    def is_link(self, obj):
        return IATLink.providedBy(obj)

    def embed_code(self, obj):
        if self.is_link(obj):
            context = aq_inner(obj)
            return context.getField('embedCode').get(context)
        return None

    def formatPerex(self, text):
        max = self.context.getField('perex_length').get(self.context)
        if len(text) < max:
            return text
        props = self.tools.properties().get('site_properties')
        if props:
            ellipsis = props.ellipsis
            return '%s%s' % (text[:max - len(ellipsis)], ellipsis)
        return text[:max]
