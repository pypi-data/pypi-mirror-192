"""
Enumerates some common technology platforms, for use with properties such as [[actionPlatform]]. It is not supposed to be comprehensive - when a suitable code is not enumerated here, textual or URL values can be used instead. These codes are at a fairly high level and do not deal with versioning and other nuance. Additional codes can be suggested [in github](https://github.com/schemaorg/schemaorg/issues/3057). 

https://schema.org/DigitalPlatformEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DigitalPlatformEnumerationInheritedProperties(TypedDict):
    """Enumerates some common technology platforms, for use with properties such as [[actionPlatform]]. It is not supposed to be comprehensive - when a suitable code is not enumerated here, textual or URL values can be used instead. These codes are at a fairly high level and do not deal with versioning and other nuance. Additional codes can be suggested [in github](https://github.com/schemaorg/schemaorg/issues/3057). 

    References:
        https://schema.org/DigitalPlatformEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DigitalPlatformEnumerationProperties(TypedDict):
    """Enumerates some common technology platforms, for use with properties such as [[actionPlatform]]. It is not supposed to be comprehensive - when a suitable code is not enumerated here, textual or URL values can be used instead. These codes are at a fairly high level and do not deal with versioning and other nuance. Additional codes can be suggested [in github](https://github.com/schemaorg/schemaorg/issues/3057). 

    References:
        https://schema.org/DigitalPlatformEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#DigitalPlatformEnumerationInheritedPropertiesTd = DigitalPlatformEnumerationInheritedProperties()
#DigitalPlatformEnumerationPropertiesTd = DigitalPlatformEnumerationProperties()


class AllProperties(DigitalPlatformEnumerationInheritedProperties , DigitalPlatformEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DigitalPlatformEnumerationProperties, DigitalPlatformEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DigitalPlatformEnumeration"
    return model
    

DigitalPlatformEnumeration = create_schema_org_model()