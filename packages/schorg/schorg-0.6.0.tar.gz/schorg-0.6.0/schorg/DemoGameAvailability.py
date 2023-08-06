"""
Indicates demo game availability, i.e. a somehow limited demonstration of the full game.

https://schema.org/DemoGameAvailability
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DemoGameAvailabilityInheritedProperties(TypedDict):
    """Indicates demo game availability, i.e. a somehow limited demonstration of the full game.

    References:
        https://schema.org/DemoGameAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    


class DemoGameAvailabilityProperties(TypedDict):
    """Indicates demo game availability, i.e. a somehow limited demonstration of the full game.

    References:
        https://schema.org/DemoGameAvailability
    Note:
        Model Depth 5
    Attributes:
    """

    

#DemoGameAvailabilityInheritedPropertiesTd = DemoGameAvailabilityInheritedProperties()
#DemoGameAvailabilityPropertiesTd = DemoGameAvailabilityProperties()


class AllProperties(DemoGameAvailabilityInheritedProperties , DemoGameAvailabilityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DemoGameAvailabilityProperties, DemoGameAvailabilityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DemoGameAvailability"
    return model
    

DemoGameAvailability = create_schema_org_model()