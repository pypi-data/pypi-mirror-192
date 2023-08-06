"""
Enumerates common size systems for different categories of products, for example "EN-13402" or "UK" for wearables or "Imperial" for screws.

https://schema.org/SizeSystemEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SizeSystemEnumerationInheritedProperties(TypedDict):
    """Enumerates common size systems for different categories of products, for example "EN-13402" or "UK" for wearables or "Imperial" for screws.

    References:
        https://schema.org/SizeSystemEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class SizeSystemEnumerationProperties(TypedDict):
    """Enumerates common size systems for different categories of products, for example "EN-13402" or "UK" for wearables or "Imperial" for screws.

    References:
        https://schema.org/SizeSystemEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#SizeSystemEnumerationInheritedPropertiesTd = SizeSystemEnumerationInheritedProperties()
#SizeSystemEnumerationPropertiesTd = SizeSystemEnumerationProperties()


class AllProperties(SizeSystemEnumerationInheritedProperties , SizeSystemEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SizeSystemEnumerationProperties, SizeSystemEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SizeSystemEnumeration"
    return model
    

SizeSystemEnumeration = create_schema_org_model()