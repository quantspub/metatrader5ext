"""
Collection of misc tools
"""

import sys
import logging
import inspect

from decimal import Decimal
from nautilus_metatrader5.common import (
    UNSET_INTEGER,
    UNSET_DOUBLE,
    UNSET_LONG,
    UNSET_DECIMAL,
    DOUBLE_INFINITY,
    INFINITY_STR,
)


logger = logging.getLogger(__name__)


# I use this just to visually emphasize it's a wrapper overridden method
def iswrapper(fn):
    return fn


class BadMessage(Exception):
    def __init__(self, text):
        self.text = text


class ClientException(Exception):
    def __init__(self, code, msg, text):
        self.code = code
        self.msg = msg
        self.text = text


class LogFunction(object):
    def __init__(self, text, logLevel):
        self.text = text
        self.logLevel = logLevel

    def __call__(self, fn):
        def newFn(origSelf, *args, **kwargs):
            if logger.getLogger().isEnabledFor(self.logLevel):
                argNames = [
                    argName
                    for argName in inspect.getfullargspec(fn)[0]
                    if argName != "self"
                ]
                logger.log(
                    self.logLevel,
                    "{} {} {} kw:{}".format(
                        self.text,
                        fn.__name__,
                        [
                            nameNarg
                            for nameNarg in zip(argNames, args)
                            if nameNarg[1] is not origSelf
                        ],
                        kwargs,
                    ),
                )
            fn(origSelf, *args)

        return newFn


def current_fn_name(parent_idx=0):
    # depth is 1 bc this is already a fn, so we need the caller
    return sys._getframe(1 + parent_idx).f_code.co_name


def setattr_log(self, var_name, var_value):
    # import code; code.interact(local=locals())
    logger.debug("%s %s %s=|%s|", self.__class__, id(self), var_name, var_value)
    super(self.__class__, self).__setattr__(var_name, var_value)


SHOW_UNSET = True


def decode(the_type, fields, show_unset=False, use_unicode=False):
    try:
        s = next(fields)
    except StopIteration:
        raise BadMessage("no more fields")

    logger.debug("decode %s %s", the_type, s)

    if the_type is Decimal:
        if (
            s is None
            or len(s) == 0
            or s.decode() == "2147483647"
            or s.decode() == "9223372036854775807"
            or s.decode() == "1.7976931348623157E308"
        ):
            return UNSET_DECIMAL
        else:
            return the_type(s.decode())

    if the_type is str:
        if type(s) is str:
            return s
        elif type(s) is bytes:
            return s.decode(
                "unicode-escape" if use_unicode else "UTF-8", errors="backslashreplace"
            )
        else:
            raise TypeError(
                "unsupported incoming type " + type(s) + " for desired type 'str"
            )

    orig_type = the_type
    if the_type is bool:
        the_type = int

    if the_type is float:
        if s.decode() == INFINITY_STR:
            return DOUBLE_INFINITY

    if show_unset:
        if s is None or len(s) == 0:
            if the_type is float:
                n = UNSET_DOUBLE
            elif the_type is int:
                n = UNSET_INTEGER
            else:
                raise TypeError("unsupported desired type for empty value" + the_type)
        else:
            n = the_type(s)
    else:
        n = the_type(s or 0)

    if orig_type is bool:
        n = False if n == 0 else True

    return n


def ExerciseStaticMethods(klass):

    import types

    # import code; code.interact(local=dict(globals(), **locals()))
    for _, var in inspect.getmembers(klass):
        # print(name, var, type(var))
        if type(var) == types.FunctionType:
            print("Exercising: %s:" % var)
            print(var())
            print()


def floatMaxString(val: float):
    return (
        "{:.8f}".format(val).rstrip("0").rstrip(".").rstrip(",")
        if val != UNSET_DOUBLE
        else ""
    )


def longMaxString(val):
    return str(val) if val != UNSET_LONG else ""


def intMaxString(val):
    return str(val) if val != UNSET_INTEGER else ""


def isAsciiPrintable(val):
    return all(ord(c) >= 32 and ord(c) < 128 for c in val)


def decimalMaxString(val: Decimal):
    return "{:f}".format(val) if val != UNSET_DECIMAL else ""


class Object(object):
    def __str__(self):
        return "Object"

    def __repr__(self):
        return str(id(self)) + ": " + self.__str__()


def MQL5parse(text):
    if text == None:
        return text
    text = text[0 : len(text) - 1]
    Array = text.split(";")
    resultArray = []
    for i in Array:
        resultArray.append(i.split(","))
    if len(Array) == 1 and len(resultArray[0]) == 1:
        return resultArray[0][0]
    return resultArray


def MQL5Period(text):
    Periods = [
        "M1",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "M10",
        "M12",
        "M15",
        "M20",
        "M30",
        "H1",
        "H2",
        "H3",
        "H4",
        "H6",
        "H8",
        "H12",
        "D1",
        "W1",
        "MN1",
    ]
    for i in Periods:
        if i == text.upper():
            return "PERIOD_" + i
    return "PERIOD_CURRENT"



# def decode_string(self, encoded_bytes: bytes) -> str:
#     """ Decodes the received bytes by reversing the shift encoding. """
#     return ''.join(chr(b - 42) for b in encoded_bytes)
    
    # def uncompress_string(self, compressed_bytes: bytes) -> bytes:
    #     """ Decompresses a run-length encoded byte sequence. """
    #     uncompressed = bytearray()
    #     i = 0
    #     while i < len(compressed_bytes):
    #         char = compressed_bytes[i]
    #         if i + 1 < len(compressed_bytes) and isinstance(compressed_bytes[i+1], int):
    #             count = compressed_bytes[i+1]
    #             uncompressed.extend([char] * count)
    #             i += 2
    #         else:
    #             uncompressed.append(char)
    #             i += 1
    #     return bytes(uncompressed)