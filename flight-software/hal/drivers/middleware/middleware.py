"""
middleware.py: Middleware class for handling faults at the driver level.

This module provides an abstract middelware class that is implemented by
each of the custom middleware classes for each component driver.

The goal of the middleware is to catch the exceptions generated by the driver
and convert them into uniquely known exceptions that can be handled by the
flight software.

Author: Harry Rosmann

"""

from ..diagnostics.diagnostics import Diagnostics
from micropython import const
from handlers import Handler

# The default number of retries for the middleware
# NOTE: Keep this value low to prevent loss of timing
FAULT_HANDLE_RETRIES = const(1)


class Middleware:
    """Middleware: Middleware class for handling faults at the driver level.

    This class provides a middleware class that wraps the driver instance and
    catches the exceptions generated by the driver. The middleware class then
    converts the exceptions into uniquely known exceptions that can be handled
    by the flight software.
    """

    def __init__(self, cls_instance: Diagnostics):
        """__init__: Constructor for the DriverMiddleware class.

        :param cls_instance: The instance of the driver class to wrap
        :param exception: The unique exception raised if fault not handled
        """
        self._wrapped_instance = cls_instance
        self._wrapped_attributes = {}
        self.wrap_handleable()

    def wrap_handleable(self):
        for name in self._wrapped_instance.handleable:
            attr = getattr(self._wrapped_instance, name)
            if callable(attr) or isinstance(attr, property):
                self._wrapped_attributes[name] = self.wrap_attribute(attr)

    def get_instance(self):
        """get_instance: Get the wrapped instance of the driver."""
        return self._wrapped_instance

    def __getattr__(self, name):
        """__getattr__: Get the attribute of the driver instance.

        :param name: The name of the attribute to get
        """
        if name in self._wrapped_attributes:
            return self._wrapped_attributes[name]
        return getattr(self._wrapped_instance, name)

    def wrap_attribute(self, attr):
        """wrap_attribute: Wrap the attribute of the driver instance.

        :param attr: The attribute to wrap
        """
        if callable(attr):
            return self.wrap_method(attr)
        elif isinstance(attr, property):
            return property(
                fget=self.wrap_method(attr.fget) if attr.fget else None,
                fset=self.wrap_method(attr.fset) if attr.fset else None,
                fdel=self.wrap_method(attr.fdel) if attr.fdel else None,
                doc=attr.__doc__,
            )
        return attr

    def wrap_method(self, method):
        """wrap_method: Wrap the method of the driver instance.

        :param method: The method to wrap
        """

        return self._wrapped_instance.handler(method)
