"""
Size group "Regular" for wearables.

https://schema.org/WearableSizeGroupRegular
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupRegularInheritedProperties(TypedDict):
    """Size group "Regular" for wearables.

    References:
        https://schema.org/WearableSizeGroupRegular
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupRegularProperties(TypedDict):
    """Size group "Regular" for wearables.

    References:
        https://schema.org/WearableSizeGroupRegular
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupRegularInheritedPropertiesTd = WearableSizeGroupRegularInheritedProperties()
#WearableSizeGroupRegularPropertiesTd = WearableSizeGroupRegularProperties()


class AllProperties(WearableSizeGroupRegularInheritedProperties , WearableSizeGroupRegularProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupRegularProperties, WearableSizeGroupRegularInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupRegular"
    return model
    

WearableSizeGroupRegular = create_schema_org_model()