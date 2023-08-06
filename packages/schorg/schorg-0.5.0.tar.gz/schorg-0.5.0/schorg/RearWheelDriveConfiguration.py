"""
Real-wheel drive is a transmission layout where the engine drives the rear wheels.

https://schema.org/RearWheelDriveConfiguration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RearWheelDriveConfigurationInheritedProperties(TypedDict):
    """Real-wheel drive is a transmission layout where the engine drives the rear wheels.

    References:
        https://schema.org/RearWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    


class RearWheelDriveConfigurationProperties(TypedDict):
    """Real-wheel drive is a transmission layout where the engine drives the rear wheels.

    References:
        https://schema.org/RearWheelDriveConfiguration
    Note:
        Model Depth 6
    Attributes:
    """

    

#RearWheelDriveConfigurationInheritedPropertiesTd = RearWheelDriveConfigurationInheritedProperties()
#RearWheelDriveConfigurationPropertiesTd = RearWheelDriveConfigurationProperties()


class AllProperties(RearWheelDriveConfigurationInheritedProperties , RearWheelDriveConfigurationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RearWheelDriveConfigurationProperties, RearWheelDriveConfigurationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RearWheelDriveConfiguration"
    return model
    

RearWheelDriveConfiguration = create_schema_org_model()