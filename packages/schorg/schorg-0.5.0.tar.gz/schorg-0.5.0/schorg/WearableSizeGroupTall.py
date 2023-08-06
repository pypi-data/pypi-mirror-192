"""
Size group "Tall" for wearables.

https://schema.org/WearableSizeGroupTall
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupTallInheritedProperties(TypedDict):
    """Size group "Tall" for wearables.

    References:
        https://schema.org/WearableSizeGroupTall
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupTallProperties(TypedDict):
    """Size group "Tall" for wearables.

    References:
        https://schema.org/WearableSizeGroupTall
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupTallInheritedPropertiesTd = WearableSizeGroupTallInheritedProperties()
#WearableSizeGroupTallPropertiesTd = WearableSizeGroupTallProperties()


class AllProperties(WearableSizeGroupTallInheritedProperties , WearableSizeGroupTallProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupTallProperties, WearableSizeGroupTallInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupTall"
    return model
    

WearableSizeGroupTall = create_schema_org_model()