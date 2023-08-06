"""
A river (for example, the broad majestic Shannon).

https://schema.org/RiverBodyOfWater
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RiverBodyOfWaterInheritedProperties(TypedDict):
    """A river (for example, the broad majestic Shannon).

    References:
        https://schema.org/RiverBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    


class RiverBodyOfWaterProperties(TypedDict):
    """A river (for example, the broad majestic Shannon).

    References:
        https://schema.org/RiverBodyOfWater
    Note:
        Model Depth 5
    Attributes:
    """

    

#RiverBodyOfWaterInheritedPropertiesTd = RiverBodyOfWaterInheritedProperties()
#RiverBodyOfWaterPropertiesTd = RiverBodyOfWaterProperties()


class AllProperties(RiverBodyOfWaterInheritedProperties , RiverBodyOfWaterProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RiverBodyOfWaterProperties, RiverBodyOfWaterInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RiverBodyOfWater"
    return model
    

RiverBodyOfWater = create_schema_org_model()