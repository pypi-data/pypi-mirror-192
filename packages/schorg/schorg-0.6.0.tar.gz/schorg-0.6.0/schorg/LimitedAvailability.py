"""
Indicates that the item has limited availability.

https://schema.org/LimitedAvailability
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LimitedAvailabilityInheritedProperties(TypedDict):
    """Indicates that the item has limited availability.

    References:
        https://schema.org/LimitedAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    


class LimitedAvailabilityProperties(TypedDict):
    """Indicates that the item has limited availability.

    References:
        https://schema.org/LimitedAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    

#LimitedAvailabilityInheritedPropertiesTd = LimitedAvailabilityInheritedProperties()
#LimitedAvailabilityPropertiesTd = LimitedAvailabilityProperties()


class AllProperties(LimitedAvailabilityInheritedProperties , LimitedAvailabilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LimitedAvailabilityProperties, LimitedAvailabilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LimitedAvailability"
    return model
    

LimitedAvailability = create_schema_org_model()