"""
Indicates the usage of the vehicle for driving school.

https://schema.org/DrivingSchoolVehicleUsage
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrivingSchoolVehicleUsageInheritedProperties(TypedDict):
    """Indicates the usage of the vehicle for driving school.

    References:
        https://schema.org/DrivingSchoolVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    


class DrivingSchoolVehicleUsageProperties(TypedDict):
    """Indicates the usage of the vehicle for driving school.

    References:
        https://schema.org/DrivingSchoolVehicleUsage
    Note:
        Model Depth 5
    Attributes:
    """

    

#DrivingSchoolVehicleUsageInheritedPropertiesTd = DrivingSchoolVehicleUsageInheritedProperties()
#DrivingSchoolVehicleUsagePropertiesTd = DrivingSchoolVehicleUsageProperties()


class AllProperties(DrivingSchoolVehicleUsageInheritedProperties , DrivingSchoolVehicleUsageProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrivingSchoolVehicleUsageProperties, DrivingSchoolVehicleUsageInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrivingSchoolVehicleUsage"
    return model
    

DrivingSchoolVehicleUsage = create_schema_org_model()