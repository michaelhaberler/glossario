"""Sample file to serve as the basis for inspect examples.
"""

import logging


LOGGER = logging.getLogger(__name__)


def c_module_level_function(arg1, arg2='default', *args, **kwargs):
    """This function is declared in the module."""
    LOGGER.debug("module_level_function, "
                 "locals = {}".format(locals()))
    local_variable = arg1
    return


class CA(object):
    """The CA class."""
    def __init__(self, name):
        self.name = name

    def get_name(self):
        "Returns the name of the instance."
        return self.name


instance_of_ca = CA('sample_instance')


class CB(CA):
    """This is the CB class.
    It is derived from CA.
    """

    # This method is not part of A.
    def do_something(self):
        """Does some work"""
        pass

    def get_name(self):
        "Overrides version from CA"
        return 'CB(' + self.name + ')'

