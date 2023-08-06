"""
A Hindu temple.

https://schema.org/HinduTemple
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HinduTempleInheritedProperties(TypedDict):
    """A Hindu temple.

    References:
        https://schema.org/HinduTemple
    Note:
        Model Depth 5
    Attributes:
    """

    


class HinduTempleProperties(TypedDict):
    """A Hindu temple.

    References:
        https://schema.org/HinduTemple
    Note:
        Model Depth 5
    Attributes:
    """

    

#HinduTempleInheritedPropertiesTd = HinduTempleInheritedProperties()
#HinduTemplePropertiesTd = HinduTempleProperties()


class AllProperties(HinduTempleInheritedProperties , HinduTempleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HinduTempleProperties, HinduTempleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HinduTemple"
    return model
    

HinduTemple = create_schema_org_model()