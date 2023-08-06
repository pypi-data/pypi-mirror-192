# isinstancex (version: 2.0.0)
#
# Copyright 2023. DuelitDev all rights reserved.
#
# This Library is distributed under the MIT License.


import typing
from isinstancex.parser import parse as _parse

__all__ = ["isinstancex", "tryinstance", "tryinstancex"]


def isinstancex(__obj: typing.Any,
                __class_or_type_hint: typing.Union[typing.Type, type, tuple]) \
        -> bool:
    """
    Return whether an object is an instance of a class or of a subclass thereof.
    A tuple or type hint,
    as in isinstancex(x, (A, B, ...)) or isinstancex(x, typing...),
    may be given as the target to check against.
    This is equivalent to isinstance(x, A) or isinstance(x, B) or ... etc.

    :param __obj: An instance.
    :param __class_or_type_hint: Class type or type hint.
    :return: bool
    """
    return _parse(__class_or_type_hint, __obj)


def tryinstance(__obj: typing.Any,
                __class_or_tuple: typing.Union[type, tuple],
                __raise_exception: type = TypeError,
                __except_message: str = "a {} is required (got type {})") \
        -> bool:
    """
    Return True or Exception whether
    an object is an instance of a class or of a subclass thereof.
    A tuple, as in isinstance(x, (A, B, ...)),
    may be given as the target to check against.
    This is equivalent to isinstance(x, A) or isinstance(x, B) or ... etc.

    :param __obj: An instance.
    :param __class_or_tuple: Class type.
    :param __raise_exception: Exception type if false.
    :param __except_message: Exception message if false.
    :return: bool
    """
    return _tryinstance(isinstance, __obj,
                        __class_or_tuple,
                        __raise_exception,
                        __except_message)


def tryinstancex(__obj: typing.Any,
                 __class_or_tuple: typing.Union[type, tuple],
                 __raise_exception: type = TypeError,
                 __except_message: str = "a {} is required (got type {})") \
        -> bool:
    """
    Return True or Exception whether
    an object is an instance of a class or of a subclass thereof.
    A tuple or type hint,
    as in isinstancex(x, (A, B, ...)) or isinstancex(x, typing...),
    may be given as the target to check against.
    This is equivalent to isinstance(x, A) or isinstance(x, B) or ... etc.

    :param __obj: An instance.
    :param __class_or_tuple: Class type.
    :param __raise_exception: Exception type if false.
    :param __except_message: Exception message if false.
    :return: bool
    """
    return _tryinstance(isinstancex, __obj,
                        __class_or_tuple,
                        __raise_exception,
                        __except_message)


def _tryinstance(__function,
                 __obj: typing.Any,
                 __class_or_tuple: typing.Union[type, tuple],
                 __raise_exception: type = TypeError,
                 __except_message: str = "a {} is required (got type {})") \
        -> bool:
    """
    Return True or Exception whether
    an object is an instance of a class or of a subclass thereof.
    A tuple, as in isinstance(x, (A, B, ...)),
    may be given as the target to check against.
    This is equivalent to isinstance(x, A) or isinstance(x, B) or ... etc.

    :param __obj: An instance.
    :param __class_or_tuple: Class type.
    :param __raise_exception: Exception type if false.
    :param __except_message: Exception message if false.
    :return: bool
    """
    # type check
    if __function(__obj, __class_or_tuple):
        return True
    # get require type name
    if __function(__class_or_tuple, tuple):
        temp = []
        for __class in __class_or_tuple:
            temp.append(__class.__name__)
        require = ", ".join(temp)
    else:
        require = __class_or_tuple.__name__
    # get the type I got
    got_type = type(__obj).__name__
    # raise
    message = __except_message.format(require, got_type)
    raise __raise_exception(message)
