"""
All-wheel Drive is a transmission layout where the engine drives all four wheels.

https://schema.org/AllWheelDriveConfiguration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AllWheelDriveConfigurationInheritedProperties(TypedDict):
    """All-wheel Drive is a transmission layout where the engine drives all four wheels.

    References:
        https://schema.org/AllWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    


class AllWheelDriveConfigurationProperties(TypedDict):
    """All-wheel Drive is a transmission layout where the engine drives all four wheels.

    References:
        https://schema.org/AllWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    

#AllWheelDriveConfigurationInheritedPropertiesTd = AllWheelDriveConfigurationInheritedProperties()
#AllWheelDriveConfigurationPropertiesTd = AllWheelDriveConfigurationProperties()


class AllProperties(AllWheelDriveConfigurationInheritedProperties , AllWheelDriveConfigurationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AllWheelDriveConfigurationProperties, AllWheelDriveConfigurationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AllWheelDriveConfiguration"
    return model
    

AllWheelDriveConfiguration = create_schema_org_model()