from typing import Any, Mapping, TypeVar

T = TypeVar("T")

def make_mapping(obj: Any, by_alias: bool = False) -> Mapping[str, Any]:
    """Receives a gyver.attrs defined class and
    returns a mapping depth-1 of the class"""
    ...

def deserialize_mapping(mapping: Mapping[str, Any]) -> Mapping[str, Any]:
    """Recursively unwraps the mapping resolving gyver classes,
    other mappings and sequences(list, set, tuple) internally"""
    ...
