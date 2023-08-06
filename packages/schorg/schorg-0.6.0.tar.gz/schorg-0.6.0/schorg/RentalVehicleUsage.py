"""
Indicates the usage of the vehicle as a rental car.

https://schema.org/RentalVehicleUsage
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RentalVehicleUsageInheritedProperties(TypedDict):
    """Indicates the usage of the vehicle as a rental car.

    References:
        https://schema.org/RentalVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    


class RentalVehicleUsageProperties(TypedDict):
    """Indicates the usage of the vehicle as a rental car.

    References:
        https://schema.org/RentalVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    

#RentalVehicleUsageInheritedPropertiesTd = RentalVehicleUsageInheritedProperties()
#RentalVehicleUsagePropertiesTd = RentalVehicleUsageProperties()


class AllProperties(RentalVehicleUsageInheritedProperties , RentalVehicleUsageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RentalVehicleUsageProperties, RentalVehicleUsageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RentalVehicleUsage"
    return model
    

RentalVehicleUsage = create_schema_org_model()