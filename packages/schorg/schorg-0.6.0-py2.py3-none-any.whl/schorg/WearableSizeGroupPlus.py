"""
Size group "Plus" for wearables.

https://schema.org/WearableSizeGroupPlus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupPlusInheritedProperties(TypedDict):
    """Size group "Plus" for wearables.

    References:
        https://schema.org/WearableSizeGroupPlus
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupPlusProperties(TypedDict):
    """Size group "Plus" for wearables.

    References:
        https://schema.org/WearableSizeGroupPlus
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupPlusInheritedPropertiesTd = WearableSizeGroupPlusInheritedProperties()
#WearableSizeGroupPlusPropertiesTd = WearableSizeGroupPlusProperties()


class AllProperties(WearableSizeGroupPlusInheritedProperties , WearableSizeGroupPlusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupPlusProperties, WearableSizeGroupPlusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupPlus"
    return model
    

WearableSizeGroupPlus = create_schema_org_model()