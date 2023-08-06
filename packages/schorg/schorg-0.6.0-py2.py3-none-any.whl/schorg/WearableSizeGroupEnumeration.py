"""
Enumerates common size groups (also known as "size types") for wearable products.

https://schema.org/WearableSizeGroupEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupEnumerationInheritedProperties(TypedDict):
    """Enumerates common size groups (also known as "size types") for wearable products.

    References:
        https://schema.org/WearableSizeGroupEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    


class WearableSizeGroupEnumerationProperties(TypedDict):
    """Enumerates common size groups (also known as "size types") for wearable products.

    References:
        https://schema.org/WearableSizeGroupEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    

#WearableSizeGroupEnumerationInheritedPropertiesTd = WearableSizeGroupEnumerationInheritedProperties()
#WearableSizeGroupEnumerationPropertiesTd = WearableSizeGroupEnumerationProperties()


class AllProperties(WearableSizeGroupEnumerationInheritedProperties , WearableSizeGroupEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupEnumerationProperties, WearableSizeGroupEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupEnumeration"
    return model
    

WearableSizeGroupEnumeration = create_schema_org_model()