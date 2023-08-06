"""
The steering position is on the left side of the vehicle (viewed from the main direction of driving).

https://schema.org/LeftHandDriving
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LeftHandDrivingInheritedProperties(TypedDict):
    """The steering position is on the left side of the vehicle (viewed from the main direction of driving).

    References:
        https://schema.org/LeftHandDriving
    Note:
        Model Depth 6
    Attributes:
    """

    


class LeftHandDrivingProperties(TypedDict):
    """The steering position is on the left side of the vehicle (viewed from the main direction of driving).

    References:
        https://schema.org/LeftHandDriving
    Note:
        Model Depth 6
    Attributes:
    """

    

#LeftHandDrivingInheritedPropertiesTd = LeftHandDrivingInheritedProperties()
#LeftHandDrivingPropertiesTd = LeftHandDrivingProperties()


class AllProperties(LeftHandDrivingInheritedProperties , LeftHandDrivingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LeftHandDrivingProperties, LeftHandDrivingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LeftHandDriving"
    return model
    

LeftHandDriving = create_schema_org_model()