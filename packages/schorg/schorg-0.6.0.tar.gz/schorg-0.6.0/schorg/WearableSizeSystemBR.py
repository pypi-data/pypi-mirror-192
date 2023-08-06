"""
Brazilian size system for wearables.

https://schema.org/WearableSizeSystemBR
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemBRInheritedProperties(TypedDict):
    """Brazilian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemBR
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemBRProperties(TypedDict):
    """Brazilian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemBR
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemBRInheritedPropertiesTd = WearableSizeSystemBRInheritedProperties()
#WearableSizeSystemBRPropertiesTd = WearableSizeSystemBRProperties()


class AllProperties(WearableSizeSystemBRInheritedProperties , WearableSizeSystemBRProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemBRProperties, WearableSizeSystemBRInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemBR"
    return model
    

WearableSizeSystemBR = create_schema_org_model()