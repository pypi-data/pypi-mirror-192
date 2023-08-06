from abc import ABC
from typing import Generic, TypeVar


class _Finder(ABC):
    pass


T = TypeVar("T")


class InstanceFinder(_Finder, Generic[T]):
    pass


class ClassFinder(_Finder, Generic[T]):
    pass
