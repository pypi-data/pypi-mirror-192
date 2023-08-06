"""
Enumerates common size systems specific for wearable products

https://schema.org/WearableSizeSystemEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemEnumerationInheritedProperties(TypedDict):
    """Enumerates common size systems specific for wearable products

    References:
        https://schema.org/WearableSizeSystemEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    


class WearableSizeSystemEnumerationProperties(TypedDict):
    """Enumerates common size systems specific for wearable products

    References:
        https://schema.org/WearableSizeSystemEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    

#WearableSizeSystemEnumerationInheritedPropertiesTd = WearableSizeSystemEnumerationInheritedProperties()
#WearableSizeSystemEnumerationPropertiesTd = WearableSizeSystemEnumerationProperties()


class AllProperties(WearableSizeSystemEnumerationInheritedProperties , WearableSizeSystemEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemEnumerationProperties, WearableSizeSystemEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemEnumeration"
    return model
    

WearableSizeSystemEnumeration = create_schema_org_model()