# isinstancex (version: 2.0.0)
#
# Copyright 2023. DuelitDev all rights reserved.
#
# This Library is distributed under the MIT License.

import typing

__all__ = ["python_version", "py_ver"]


class _PythonVersion:
    __ver__: int = __import__("sys").version_info.minor

    @staticmethod
    def _parse(ver: typing.Union[int, float]) -> int:
        if isinstance(ver, float):
            return int(str(ver).split(".")[1])
        return ver

    def __gt__(self, other: typing.Union[int, float]) -> bool:
        return self.__ver__ > self._parse(other)

    def __ge__(self, other: typing.Union[int, float]) -> bool:
        return self.__ver__ >= self._parse(other)

    def __lt__(self, other: typing.Union[int, float]) -> bool:
        return self.__ver__ < self._parse(other)

    def __le__(self, other: typing.Union[int, float]) -> bool:
        return self.__ver__ <= self._parse(other)

    def __eq__(self, other: typing.Union[int, float]) -> bool:
        return self.__ver__ == self._parse(other)

    def __ne__(self, other: typing.Union[int, float]) -> bool:
        return not self == other


python_version = _PythonVersion()
py_ver = python_version
