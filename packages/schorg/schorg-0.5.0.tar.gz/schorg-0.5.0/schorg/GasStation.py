"""
A gas station.

https://schema.org/GasStation
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GasStationInheritedProperties(TypedDict):
    """A gas station.

    References:
        https://schema.org/GasStation
    Note:
        Model Depth 5
    Attributes:
    """

    


class GasStationProperties(TypedDict):
    """A gas station.

    References:
        https://schema.org/GasStation
    Note:
        Model Depth 5
    Attributes:
    """

    

#GasStationInheritedPropertiesTd = GasStationInheritedProperties()
#GasStationPropertiesTd = GasStationProperties()


class AllProperties(GasStationInheritedProperties , GasStationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GasStationProperties, GasStationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GasStation"
    return model
    

GasStation = create_schema_org_model()