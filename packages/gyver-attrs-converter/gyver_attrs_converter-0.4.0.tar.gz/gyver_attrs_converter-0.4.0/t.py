from gyver.attrs import define, info
from timeit import timeit
from gattrs_converter import deserialize, make_mapping, deserialize_mapping


@define
class D:
    d: str = info(alias="dKey")

    def __parse_dict__(self, alias: bool):
        return {"dKey": self.d} if alias else {"d": self.d}


@define
class C:
    c: tuple[D, ...] = info(alias="cKey")

    def __parse_dict__(self, alias: bool):
        if alias:
            return {
                "cKey": tuple(item.__parse_dict__(alias) for item in self.c)
            }
        return {"c": tuple(item.__parse_dict__(alias) for item in self.c)}


@define
class B:
    b: C = info(alias="bKey")

    def __parse_dict__(self, alias: bool):
        if alias:
            return {"bKey": self.b.__parse_dict__(alias)}
        return {"b": self.b.__parse_dict__(alias)}


@define
class A:
    a: B = info(alias="aKey")

    def __parse_dict__(self, alias: bool):
        if alias:
            return {"aKey": self.a.__parse_dict__(alias)}
        return {"a": self.a.__parse_dict__(alias)}


obj = A(B(C(tuple(D("other") for _ in range(35)))))
print(deserialize(make_mapping(obj, True)))
print(timeit(lambda: deserialize_mapping(make_mapping(obj, True), True)))
