"""
GS1 (formerly NRF) size system for wearables.

https://schema.org/WearableSizeSystemGS1
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemGS1InheritedProperties(TypedDict):
    """GS1 (formerly NRF) size system for wearables.

    References:
        https://schema.org/WearableSizeSystemGS1
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemGS1Properties(TypedDict):
    """GS1 (formerly NRF) size system for wearables.

    References:
        https://schema.org/WearableSizeSystemGS1
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemGS1InheritedPropertiesTd = WearableSizeSystemGS1InheritedProperties()
#WearableSizeSystemGS1PropertiesTd = WearableSizeSystemGS1Properties()


class AllProperties(WearableSizeSystemGS1InheritedProperties , WearableSizeSystemGS1Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemGS1Properties, WearableSizeSystemGS1InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemGS1"
    return model
    

WearableSizeSystemGS1 = create_schema_org_model()