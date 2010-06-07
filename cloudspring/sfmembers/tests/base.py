import cloudspring.sfmembers

from Products.Five import zcml

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    
    zcml.load_config('configure.zcml', cloudspring.sfmembers)

    
setup_product()
ptc.setupPloneSite(products=['cloudspring.sfmembers'])



class IntegrationTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """



