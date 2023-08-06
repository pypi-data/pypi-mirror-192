"""
French size system for wearables.

https://schema.org/WearableSizeSystemFR
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemFRInheritedProperties(TypedDict):
    """French size system for wearables.

    References:
        https://schema.org/WearableSizeSystemFR
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemFRProperties(TypedDict):
    """French size system for wearables.

    References:
        https://schema.org/WearableSizeSystemFR
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemFRInheritedPropertiesTd = WearableSizeSystemFRInheritedProperties()
#WearableSizeSystemFRPropertiesTd = WearableSizeSystemFRProperties()


class AllProperties(WearableSizeSystemFRInheritedProperties , WearableSizeSystemFRProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemFRProperties, WearableSizeSystemFRInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemFR"
    return model
    

WearableSizeSystemFR = create_schema_org_model()