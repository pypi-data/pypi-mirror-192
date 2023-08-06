"""
German size system for wearables.

https://schema.org/WearableSizeSystemDE
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemDEInheritedProperties(TypedDict):
    """German size system for wearables.

    References:
        https://schema.org/WearableSizeSystemDE
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemDEProperties(TypedDict):
    """German size system for wearables.

    References:
        https://schema.org/WearableSizeSystemDE
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemDEInheritedPropertiesTd = WearableSizeSystemDEInheritedProperties()
#WearableSizeSystemDEPropertiesTd = WearableSizeSystemDEProperties()


class AllProperties(WearableSizeSystemDEInheritedProperties , WearableSizeSystemDEProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemDEProperties, WearableSizeSystemDEInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemDE"
    return model
    

WearableSizeSystemDE = create_schema_org_model()