"""
A Buddhist temple.

https://schema.org/BuddhistTemple
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BuddhistTempleInheritedProperties(TypedDict):
    """A Buddhist temple.

    References:
        https://schema.org/BuddhistTemple
    Note:
        Model Depth 5
    Attributes:
    """

    


class BuddhistTempleProperties(TypedDict):
    """A Buddhist temple.

    References:
        https://schema.org/BuddhistTemple
    Note:
        Model Depth 5
    Attributes:
    """

    

#BuddhistTempleInheritedPropertiesTd = BuddhistTempleInheritedProperties()
#BuddhistTemplePropertiesTd = BuddhistTempleProperties()


class AllProperties(BuddhistTempleInheritedProperties , BuddhistTempleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BuddhistTempleProperties, BuddhistTempleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BuddhistTemple"
    return model
    

BuddhistTemple = create_schema_org_model()