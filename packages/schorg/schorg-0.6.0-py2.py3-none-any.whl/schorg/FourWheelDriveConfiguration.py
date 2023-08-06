"""
Four-wheel drive is a transmission layout where the engine primarily drives two wheels with a part-time four-wheel drive capability.

https://schema.org/FourWheelDriveConfiguration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FourWheelDriveConfigurationInheritedProperties(TypedDict):
    """Four-wheel drive is a transmission layout where the engine primarily drives two wheels with a part-time four-wheel drive capability.

    References:
        https://schema.org/FourWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    


class FourWheelDriveConfigurationProperties(TypedDict):
    """Four-wheel drive is a transmission layout where the engine primarily drives two wheels with a part-time four-wheel drive capability.

    References:
        https://schema.org/FourWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    

#FourWheelDriveConfigurationInheritedPropertiesTd = FourWheelDriveConfigurationInheritedProperties()
#FourWheelDriveConfigurationPropertiesTd = FourWheelDriveConfigurationProperties()


class AllProperties(FourWheelDriveConfigurationInheritedProperties , FourWheelDriveConfigurationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FourWheelDriveConfigurationProperties, FourWheelDriveConfigurationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FourWheelDriveConfiguration"
    return model
    

FourWheelDriveConfiguration = create_schema_org_model()