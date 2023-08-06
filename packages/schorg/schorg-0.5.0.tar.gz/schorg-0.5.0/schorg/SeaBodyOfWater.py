"""
A sea (for example, the Caspian sea).

https://schema.org/SeaBodyOfWater
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SeaBodyOfWaterInheritedProperties(TypedDict):
    """A sea (for example, the Caspian sea).

    References:
        https://schema.org/SeaBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    


class SeaBodyOfWaterProperties(TypedDict):
    """A sea (for example, the Caspian sea).

    References:
        https://schema.org/SeaBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    

#SeaBodyOfWaterInheritedPropertiesTd = SeaBodyOfWaterInheritedProperties()
#SeaBodyOfWaterPropertiesTd = SeaBodyOfWaterProperties()


class AllProperties(SeaBodyOfWaterInheritedProperties , SeaBodyOfWaterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SeaBodyOfWaterProperties, SeaBodyOfWaterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SeaBodyOfWater"
    return model
    

SeaBodyOfWater = create_schema_org_model()