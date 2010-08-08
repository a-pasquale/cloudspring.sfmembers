import logging                                                                     
logger = logging.getLogger('SFmap')
                               
class SalesforceLookupException(Exception):
    pass

class SalesforceUpdateException(Exception):
    pass

class SFField(object):
    
    def __init__(self, field):
        self.__name__ = field
    
    def __get__(self, obj, objtype):
        k = obj._sf2py[self.__name__]
        if k in obj._dirty:
            return obj._dirty[k]
        else:
            val = getattr(obj._data, self.__name__)
            if isinstance(val, basestring):
                val = unicode(val, 'utf-8')
            return val
    
    def __set__(self, obj, value):
        k = obj._sf2py[self.__name__]
        obj._dirty[k] = value

DEFAULT_CONN = None
def set_sf_connection(conn):
    global DEFAULT_CONN
    DEFAULT_CONN = conn
    logger.info("DEFAULT_CONN " + DEFAULT_CONN)

class SFObject(object):
    """ Abstract class for classes providing read/write to objects in Salesforce.
    
    First we need to set up a connection to Salesforce...
      >>> from beatbox import PythonClient
      >>> client = PythonClient()
      >>> set_sf_connection(client)
      >>> assert sfconfig is not None
      >>> res = client.login(sfconfig.USERNAME, sfconfig.PASSWORD)
    
    Set up: clean up from previous test runs and create a new Account:
      >>> res = client.query("SELECT Id FROM Account WHERE Name = 'Foo' OR NAME = 'Bar'")
      >>> if len(res):
      ...     res = client.delete([r['Id'] for r in res])
      >>> res = client.create({'type': 'Account', 'Name': 'Foo'})
     
    An example class might provide access to Account records::
      >>> class SFAccount(SFObject):
      ...     _sObjectType = 'Account'
      ...     id = SFField('Id')
      ...     name = SFField('Name')
    
    Get an instance corresponding to an account name 'Foo'::
      >>> foo = SFAccount("Name = 'Foo'")
    
    Now we can access the values that were retrieved from Salesforce.com when
    the object was instantiated::
      >>> foo.name
      'Foo'
    
    We can also modify values:
      >>> foo.name = 'Bar'
    
    Following modifications, we see the modified value on the object:
      >>> foo.name
      'Bar'
    
    However, the change hasn't yet been saved back to the database:
      >>> not_bar = SFAccount("Name = 'Bar'")
      Traceback (most recent call last):
        ...
      SalesforceLookupException: No records found.
      
    To actually write the modifications back to Salesforce, we must call the
    update method (this way, we can wait to save multiple changes until we're
    done)::
      >>> foo.update()
    
    Now a newly instantiated SFAccount, based on the first one's Id, should
    have the new name::
    
      >>> bar = SFAccount("Id='%s'" % foo.id)
      >>> bar.name
      'Bar'
    """
    
    _sObjectType = None
    _sf2py = {}
    _py2sf = {}
    _data = None
    _dirty = {}
    
    def _initialize_fieldmap(self):
        """ Sets up internal mappings between Salesforce field names and SFObject attribute names."""
        if self.__class__._sf2py:
            return
        for name, field in self.__class__.__dict__.items():
            if isinstance(field, SFField):
                self.__class__._sf2py[field.__name__] = name
                self.__class__._py2sf[name] = field.__name__
    
    def _load_data(self, query=None):
        fields = ','.join(self._sf2py.keys())
        soql = "SELECT %s FROM %s" % (fields, self._sObjectType)
        logger.info('query: %s ' % query)
        if query is not None:
            soql += ' WHERE %s' % query
        logger.info('soql: %s' % soql)
        res = self.conn.query(soql)
        if not len(res):
            raise SalesforceLookupException('No records found.')
        if len(res) > 1:
            raise SalesforceLookupException('Multiple records found.')
        self._data = res[0]
    
    def __init__(self, conn=None, query=None):
        # XXX allow use as an adapter of a QueryRecord that was already found
        assert self._sObjectType is not None
        logger.info('query: ' + query)
        if conn is None:
            conn = DEFAULT_CONN
        assert conn is not None
        self.conn = conn
        self._initialize_fieldmap()
        if query is not None:
            self._load_data(query)

    def update(self, id=None, **kw):
        logger.info("id = " + id)
        logger.info("self._data['Id'] = " + self._data['Id'])
        if id is None:
            id = self._data['Id']
        rec = {
            'type': self._sObjectType,
            'sf_id__c': id,
            'Id': 'apasquale',
        }
        for k, v in self._dirty.items():
            rec[self._py2sf[k]] = v
        for k, v in kw.items():
            rec[self._py2sf[k]] = v
        res = self.conn.update(rec)
        if len(res[0]['errors']):
            raise SalesforceUpdateException(res[0]['errors'][0]['message'])
        if self._data:
            for k, v in rec.items():
                setattr(self._data, k, v)
        self._dirty = {}

if __name__ == '__main__':
    import doctest
    import sfconfig
    doctest.testmod()

