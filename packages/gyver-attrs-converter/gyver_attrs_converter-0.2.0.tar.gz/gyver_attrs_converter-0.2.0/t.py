from gyver.attrs import define, info
from timeit import timeit
from gattrs_converter import make_mapping, deserialize_mapping


@define
class D:
    d: str = info(alias="dKey")


@define
class C:
    c: tuple[D, ...] = info(alias="cKey")


@define
class B:
    b: C = info(alias="bKey")


@define
class A:
    a: B = info(alias="aKey")


obj = A(B(C(tuple(D("other") for _ in range(10)))))

print(deserialize_mapping(make_mapping(obj)))
