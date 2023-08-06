"""
Size group "Misses" (also known as "Missy") for wearables.

https://schema.org/WearableSizeGroupMisses
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupMissesInheritedProperties(TypedDict):
    """Size group "Misses" (also known as "Missy") for wearables.

    References:
        https://schema.org/WearableSizeGroupMisses
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupMissesProperties(TypedDict):
    """Size group "Misses" (also known as "Missy") for wearables.

    References:
        https://schema.org/WearableSizeGroupMisses
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupMissesInheritedPropertiesTd = WearableSizeGroupMissesInheritedProperties()
#WearableSizeGroupMissesPropertiesTd = WearableSizeGroupMissesProperties()


class AllProperties(WearableSizeGroupMissesInheritedProperties , WearableSizeGroupMissesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupMissesProperties, WearableSizeGroupMissesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupMisses"
    return model
    

WearableSizeGroupMisses = create_schema_org_model()