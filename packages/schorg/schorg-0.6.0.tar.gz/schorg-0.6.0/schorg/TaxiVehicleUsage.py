"""
Indicates the usage of the car as a taxi.

https://schema.org/TaxiVehicleUsage
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TaxiVehicleUsageInheritedProperties(TypedDict):
    """Indicates the usage of the car as a taxi.

    References:
        https://schema.org/TaxiVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    


class TaxiVehicleUsageProperties(TypedDict):
    """Indicates the usage of the car as a taxi.

    References:
        https://schema.org/TaxiVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    

#TaxiVehicleUsageInheritedPropertiesTd = TaxiVehicleUsageInheritedProperties()
#TaxiVehicleUsagePropertiesTd = TaxiVehicleUsageProperties()


class AllProperties(TaxiVehicleUsageInheritedProperties , TaxiVehicleUsageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TaxiVehicleUsageProperties, TaxiVehicleUsageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TaxiVehicleUsage"
    return model
    

TaxiVehicleUsage = create_schema_org_model()