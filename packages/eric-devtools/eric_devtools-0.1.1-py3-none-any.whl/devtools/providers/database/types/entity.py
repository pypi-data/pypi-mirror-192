from typing import TypeVar

T = TypeVar("T")


class EntityLike:
    pass


def entity_factory(name: str, suffix: str = "Entity"):
    class Entity:
        pass


Entity = entity_factory("Entity")
