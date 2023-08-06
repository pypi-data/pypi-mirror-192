"""
A lake (for example, Lake Pontrachain).

https://schema.org/LakeBodyOfWater
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LakeBodyOfWaterInheritedProperties(TypedDict):
    """A lake (for example, Lake Pontrachain).

    References:
        https://schema.org/LakeBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    


class LakeBodyOfWaterProperties(TypedDict):
    """A lake (for example, Lake Pontrachain).

    References:
        https://schema.org/LakeBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    

#LakeBodyOfWaterInheritedPropertiesTd = LakeBodyOfWaterInheritedProperties()
#LakeBodyOfWaterPropertiesTd = LakeBodyOfWaterProperties()


class AllProperties(LakeBodyOfWaterInheritedProperties , LakeBodyOfWaterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LakeBodyOfWaterProperties, LakeBodyOfWaterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LakeBodyOfWater"
    return model
    

LakeBodyOfWater = create_schema_org_model()