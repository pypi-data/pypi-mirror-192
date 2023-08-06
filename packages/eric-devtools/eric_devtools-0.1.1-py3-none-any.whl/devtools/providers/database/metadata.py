import pathlib

from devtools.providers.database.types.entity import Entity
from devtools.utils.autodiscovery import ClassFinder


def get_metadata(path: pathlib.Path):
    ClassFinder(Entity, path=path).find()
    return Entity.metadata
