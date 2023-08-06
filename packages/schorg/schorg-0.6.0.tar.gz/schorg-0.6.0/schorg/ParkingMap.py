"""
A parking map.

https://schema.org/ParkingMap
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ParkingMapInheritedProperties(TypedDict):
    """A parking map.

    References:
        https://schema.org/ParkingMap
    Note:
        Model Depth 5
    Attributes:
    """

    


class ParkingMapProperties(TypedDict):
    """A parking map.

    References:
        https://schema.org/ParkingMap
    Note:
        Model Depth 5
    Attributes:
    """

    

#ParkingMapInheritedPropertiesTd = ParkingMapInheritedProperties()
#ParkingMapPropertiesTd = ParkingMapProperties()


class AllProperties(ParkingMapInheritedProperties , ParkingMapProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ParkingMapProperties, ParkingMapInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ParkingMap"
    return model
    

ParkingMap = create_schema_org_model()