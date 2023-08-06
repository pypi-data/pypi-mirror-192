"""
A body of water, such as a sea, ocean, or lake.

https://schema.org/BodyOfWater
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyOfWaterInheritedProperties(TypedDict):
    """A body of water, such as a sea, ocean, or lake.

    References:
        https://schema.org/BodyOfWater
    Note:
        Model Depth 4
    Attributes:
    """

    


class BodyOfWaterProperties(TypedDict):
    """A body of water, such as a sea, ocean, or lake.

    References:
        https://schema.org/BodyOfWater
    Note:
        Model Depth 4
    Attributes:
    """

    

#BodyOfWaterInheritedPropertiesTd = BodyOfWaterInheritedProperties()
#BodyOfWaterPropertiesTd = BodyOfWaterProperties()


class AllProperties(BodyOfWaterInheritedProperties , BodyOfWaterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyOfWaterProperties, BodyOfWaterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyOfWater"
    return model
    

BodyOfWater = create_schema_org_model()