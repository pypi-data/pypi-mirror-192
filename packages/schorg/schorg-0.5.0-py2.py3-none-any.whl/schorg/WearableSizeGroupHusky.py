"""
Size group "Husky" (or "Stocky") for wearables.

https://schema.org/WearableSizeGroupHusky
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupHuskyInheritedProperties(TypedDict):
    """Size group "Husky" (or "Stocky") for wearables.

    References:
        https://schema.org/WearableSizeGroupHusky
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupHuskyProperties(TypedDict):
    """Size group "Husky" (or "Stocky") for wearables.

    References:
        https://schema.org/WearableSizeGroupHusky
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupHuskyInheritedPropertiesTd = WearableSizeGroupHuskyInheritedProperties()
#WearableSizeGroupHuskyPropertiesTd = WearableSizeGroupHuskyProperties()


class AllProperties(WearableSizeGroupHuskyInheritedProperties , WearableSizeGroupHuskyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupHuskyProperties, WearableSizeGroupHuskyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupHusky"
    return model
    

WearableSizeGroupHusky = create_schema_org_model()