"""Sample file to serve as the basis for inspect examples.
"""

import logging
import lib_example_a
from lib_example_c import CA
from lib_example_c import CB as ExCB


LOGGER = logging.getLogger(__name__)


def module_level_function(arg1, arg2='default', *args, **kwargs):
    """This function is declared in the module."""
    LOGGER.debug("module_level_function, "
                 "locals = {}".format(locals()))
    local_variable = arg1
    return


class BA(object):
    """The BA class."""
    def __init__(self, name):
        self.name = name
        self.a = lib_example_a.A("lib_example_a.A")
        self.ca = CA("CA")

    def get_name(self):
        "Returns the name of the instance."
        return self.name


instance_of_a = BA('sample_instance')


class BB(BA):
    """This is the B class.
    It is derived from A.
    """

    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self):
        "Overrides version from A"
        return 'BB(' + self.name + ')'

