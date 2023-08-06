"""
Size group "Girls" for wearables.

https://schema.org/WearableSizeGroupGirls
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupGirlsInheritedProperties(TypedDict):
    """Size group "Girls" for wearables.

    References:
        https://schema.org/WearableSizeGroupGirls
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupGirlsProperties(TypedDict):
    """Size group "Girls" for wearables.

    References:
        https://schema.org/WearableSizeGroupGirls
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupGirlsInheritedPropertiesTd = WearableSizeGroupGirlsInheritedProperties()
#WearableSizeGroupGirlsPropertiesTd = WearableSizeGroupGirlsProperties()


class AllProperties(WearableSizeGroupGirlsInheritedProperties , WearableSizeGroupGirlsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupGirlsProperties, WearableSizeGroupGirlsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupGirls"
    return model
    

WearableSizeGroupGirls = create_schema_org_model()