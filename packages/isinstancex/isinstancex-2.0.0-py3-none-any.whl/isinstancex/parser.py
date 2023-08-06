# isinstancex (version: 2.0.0)
#
# Copyright 2023. DuelitDev all rights reserved.
#
# This Library is distributed under the MIT License.

import typing
from isinstancex._version import *

__all__ = ["TypeHintChecker", "parse"]


class TypeHintChecker:
    def __init__(self, expression: typing.Type):
        self._expr: typing.Type = expression

    @property
    def is_hint(self) -> bool:
        return (self.is_any or self.is_union or self.is_tuple or
                self.is_list or self.is_dict or self.is_set)

    @property
    def is_any(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.11 and name == "_AnyMeta" and lib == "typing") or
                (name == "_SpecialForm" and lib == "typing" and
                 getattr(self._expr, "_name") == "Any"))

    @property
    def is_union(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.10 and name == "UnionType" and lib == "types") or
                (name == "_UnionGenericAlias" and lib == "typing"))

    @property
    def is_tuple(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.9 and name == "GenericAlias" and
                 lib == "builtins" and self._expr() == ()) or
                (name == "_GenericAlias" and lib == "typing" and
                 getattr(self._expr, "_name") == "Tuple"))

    @property
    def is_list(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.9 and name == "GenericAlias" and
                 lib == "builtins" and self._expr() == []) or
                (name == "_GenericAlias" and lib == "typing" and
                 getattr(self._expr, "_name") == "List"))

    @property
    def is_dict(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.9 and name == "GenericAlias" and
                 lib == "builtins" and self._expr() == {}) or
                (name == "_GenericAlias" and lib == "typing" and
                 getattr(self._expr, "_name") == "Dict"))

    @property
    def is_set(self) -> bool:
        name, lib = type(self._expr).__name__, self._expr.__module__
        return ((py_ver >= 3.9 and name == "GenericAlias" and
                 lib == "builtins" and self._expr() == set()) or
                (name == "_GenericAlias" and lib == "typing" and
                 getattr(self._expr, "_name") == "Set"))


def parse(expr, nodes):
    for t, i in zip((expr,), (nodes,)):
        hint = TypeHintChecker(t)
        if hint.is_hint:
            if hint.is_any:
                return True
            if hint.is_union:
                return any([parse(j, i) for j in t.__args__])
            if hint.is_tuple:
                return (isinstance(i, tuple) and
                        all([parse(j, k) for j, k in zip(t.__args__, i)]))
            if hint.is_list:
                return (isinstance(i, list) and
                        all([parse(t.__args__[0], k) for k in i]))
            if hint.is_dict:
                return (isinstance(i, dict) and
                        all([parse(t.__args__[0], k) for k in i]) and
                        all([parse(t.__args__[1], k) for k in i.values()]))
            if hint.is_set:
                return (isinstance(i, set) and
                        all([parse(t.__args__[0], k) for k in i]))
        return isinstance(i, t)
