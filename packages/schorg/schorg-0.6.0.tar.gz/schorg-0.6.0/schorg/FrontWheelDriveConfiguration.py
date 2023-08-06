"""
Front-wheel drive is a transmission layout where the engine drives the front wheels.

https://schema.org/FrontWheelDriveConfiguration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FrontWheelDriveConfigurationInheritedProperties(TypedDict):
    """Front-wheel drive is a transmission layout where the engine drives the front wheels.

    References:
        https://schema.org/FrontWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    


class FrontWheelDriveConfigurationProperties(TypedDict):
    """Front-wheel drive is a transmission layout where the engine drives the front wheels.

    References:
        https://schema.org/FrontWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    

#FrontWheelDriveConfigurationInheritedPropertiesTd = FrontWheelDriveConfigurationInheritedProperties()
#FrontWheelDriveConfigurationPropertiesTd = FrontWheelDriveConfigurationProperties()


class AllProperties(FrontWheelDriveConfigurationInheritedProperties , FrontWheelDriveConfigurationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FrontWheelDriveConfigurationProperties, FrontWheelDriveConfigurationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FrontWheelDriveConfiguration"
    return model
    

FrontWheelDriveConfiguration = create_schema_org_model()