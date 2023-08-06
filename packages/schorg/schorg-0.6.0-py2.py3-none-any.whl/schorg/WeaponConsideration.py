"""
The item is intended to induce bodily harm, for example guns, mace, combat knives, brass knuckles, nail or other bombs, and spears.

https://schema.org/WeaponConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WeaponConsiderationInheritedProperties(TypedDict):
    """The item is intended to induce bodily harm, for example guns, mace, combat knives, brass knuckles, nail or other bombs, and spears.

    References:
        https://schema.org/WeaponConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class WeaponConsiderationProperties(TypedDict):
    """The item is intended to induce bodily harm, for example guns, mace, combat knives, brass knuckles, nail or other bombs, and spears.

    References:
        https://schema.org/WeaponConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#WeaponConsiderationInheritedPropertiesTd = WeaponConsiderationInheritedProperties()
#WeaponConsiderationPropertiesTd = WeaponConsiderationProperties()


class AllProperties(WeaponConsiderationInheritedProperties , WeaponConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WeaponConsiderationProperties, WeaponConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WeaponConsideration"
    return model
    

WeaponConsideration = create_schema_org_model()