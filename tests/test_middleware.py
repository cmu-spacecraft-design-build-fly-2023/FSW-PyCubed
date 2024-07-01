import sys

import pytest

sys.path.insert(0, "./emulator/drivers/")
from middleware.generic_driver import Driver  # noqa: E402
from middleware.middleware import Middleware  # noqa: E402

"""
setting up things for an emulated test
"""


class TestException(Exception):
    def __init__(self, exception: Exception):
        self.exception = exception
        super().__init__()

    def __str__(self):
        return f"{type(self.exception).__name__}: {self.exception}"


class TestDevice(Driver):
    def __init__(self, flags: int):
        """
        flags: 2 bit flag register
            - 0: ciritcal error
            - 1: fixable error
            - 2: fixable, hidden error
        """
        self.flags = flags
        self.int_val = 8
        self.__test_str = "test"
        self.update_int = 0
        self.__property = 89

        super().__init__()

        self.handleable = {
            "get_test_int": (self.int_checker, TestException),
            "set_test_int": (lambda x, y: True, TestException),
            "test_method": (lambda x, y: x, TestException),
        }

    def get_test_int(self) -> int:
        if self.flags & 0b001:
            # best we can do is try again
            raise TestException("Critical Error")
        if self.flags & 0b010:
            raise TestException("Fixable Error")
        return self.int_val

    def set_test_int(self, input: int) -> None:
        self.int_val = input

    def get_test_str(self) -> int:
        return self.__test_str

    def set_test_str(self, input: str) -> None:
        self.__test_str = input

    def int_checker(self, result, flags):
        if "hidden" in flags:
            return False
        if result > 9:
            return False
        return True

    def test_method(self):
        self.update_int += 1
        return 9

    def unhandled_method(self, num):
        return num + 1

    def get_flags(self):
        res = {}
        if self.flags & 0b100:
            res["hidden"] = self.fixer
        if self.flags & 0b010:
            # fixable flag is raised
            res["fixable"] = self.fixer
        if self.flags & 0b001:
            # critical flag is raised
            res["critical"] = None
        return res

    def fixer(self):
        # remove the fixable flag
        self.flags = self.flags & 0b001


class TestClass:
    def test_method_call(self):
        device = TestDevice(0)
        mid = Middleware(device)

        # test normal handled method
        assert mid.get_test_int() == device.get_test_int()
        assert mid.get_test_int() == 8

        # test handled method with side effects
        assert mid.test_method() == 9
        assert mid.test_method() == device.test_method()
        assert mid.update_int == 3

        # test unhandled method
        assert mid.unhandled_method(9) == 10
        assert mid.unhandled_method(1) == device.unhandled_method(1)

    def test_method_setters(self):
        # test handled property test_int
        device = TestDevice(0)
        mid = Middleware(device)
        assert mid.get_test_int() == 8
        assert device.get_test_int() == 8
        mid.set_test_int(5)
        assert mid.get_test_int() == 5
        assert device.get_test_int() == 5

        # test unhandled property test_str
        assert mid.get_test_str() == "test"
        mid.set_test_str("testing")
        assert mid.get_test_str() == "testing"
        assert device.get_test_str() == "testing"

    def test_exceptions(self):
        """
        This test ensures that the middleware can call the flag fixer functions in order to
        get a correct result from the device.
        """
        device = TestDevice(0b010)
        mid = Middleware(device)
        with pytest.raises(TestException):
            device.get_test_int()
        assert mid.get_test_int() == 8

        device = TestDevice(0b100)
        mid = Middleware(device)
        assert mid.get_test_int() == 8

        device = TestDevice(0b001)
        mid = Middleware(device)
        with pytest.raises(TestException):
            mid.get_test_int()
