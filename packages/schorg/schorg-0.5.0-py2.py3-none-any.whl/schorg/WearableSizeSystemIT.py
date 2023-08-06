"""
Italian size system for wearables.

https://schema.org/WearableSizeSystemIT
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemITInheritedProperties(TypedDict):
    """Italian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemIT
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemITProperties(TypedDict):
    """Italian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemIT
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemITInheritedPropertiesTd = WearableSizeSystemITInheritedProperties()
#WearableSizeSystemITPropertiesTd = WearableSizeSystemITProperties()


class AllProperties(WearableSizeSystemITInheritedProperties , WearableSizeSystemITProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemITProperties, WearableSizeSystemITInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemIT"
    return model
    

WearableSizeSystemIT = create_schema_org_model()