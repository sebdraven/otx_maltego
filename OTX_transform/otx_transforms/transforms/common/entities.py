from canari.maltego.message import *

__author__ = 'slarinier'
__copyright__ = 'Copyright 2019, canari Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'slarinier'
__email__ = 'Nadeem Douba'
__status__ = 'Development'


class Pulse(Entity):
    _category_ = 'Infrastructure'
    _namespace_ = 'OTX'

    properties_pulse = StringEntityField('properties.pulse', display_name='Pulse', is_value=True)
    URL = StringEntityField('URL', display_name='None')
    ID = StringEntityField('ID', display_name='None')

