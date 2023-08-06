"""
Mexican size system for wearables.

https://schema.org/WearableSizeSystemMX
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemMXInheritedProperties(TypedDict):
    """Mexican size system for wearables.

    References:
        https://schema.org/WearableSizeSystemMX
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemMXProperties(TypedDict):
    """Mexican size system for wearables.

    References:
        https://schema.org/WearableSizeSystemMX
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemMXInheritedPropertiesTd = WearableSizeSystemMXInheritedProperties()
#WearableSizeSystemMXPropertiesTd = WearableSizeSystemMXProperties()


class AllProperties(WearableSizeSystemMXInheritedProperties , WearableSizeSystemMXProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemMXProperties, WearableSizeSystemMXInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemMX"
    return model
    

WearableSizeSystemMX = create_schema_org_model()