"""
An ocean (for example, the Pacific).

https://schema.org/OceanBodyOfWater
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OceanBodyOfWaterInheritedProperties(TypedDict):
    """An ocean (for example, the Pacific).

    References:
        https://schema.org/OceanBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    


class OceanBodyOfWaterProperties(TypedDict):
    """An ocean (for example, the Pacific).

    References:
        https://schema.org/OceanBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    

#OceanBodyOfWaterInheritedPropertiesTd = OceanBodyOfWaterInheritedProperties()
#OceanBodyOfWaterPropertiesTd = OceanBodyOfWaterProperties()


class AllProperties(OceanBodyOfWaterInheritedProperties , OceanBodyOfWaterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OceanBodyOfWaterProperties, OceanBodyOfWaterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OceanBodyOfWater"
    return model
    

OceanBodyOfWater = create_schema_org_model()