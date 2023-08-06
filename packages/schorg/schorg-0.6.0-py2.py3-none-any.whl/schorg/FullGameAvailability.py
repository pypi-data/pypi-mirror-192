"""
Indicates full game availability.

https://schema.org/FullGameAvailability
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FullGameAvailabilityInheritedProperties(TypedDict):
    """Indicates full game availability.

    References:
        https://schema.org/FullGameAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    


class FullGameAvailabilityProperties(TypedDict):
    """Indicates full game availability.

    References:
        https://schema.org/FullGameAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    

#FullGameAvailabilityInheritedPropertiesTd = FullGameAvailabilityInheritedProperties()
#FullGameAvailabilityPropertiesTd = FullGameAvailabilityProperties()


class AllProperties(FullGameAvailabilityInheritedProperties , FullGameAvailabilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FullGameAvailabilityProperties, FullGameAvailabilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FullGameAvailability"
    return model
    

FullGameAvailability = create_schema_org_model()