"""
Represents the broad notion of Android-based operating systems.

https://schema.org/AndroidPlatform
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AndroidPlatformInheritedProperties(TypedDict):
    """Represents the broad notion of Android-based operating systems.

    References:
        https://schema.org/AndroidPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    


class AndroidPlatformProperties(TypedDict):
    """Represents the broad notion of Android-based operating systems.

    References:
        https://schema.org/AndroidPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    

#AndroidPlatformInheritedPropertiesTd = AndroidPlatformInheritedProperties()
#AndroidPlatformPropertiesTd = AndroidPlatformProperties()


class AllProperties(AndroidPlatformInheritedProperties , AndroidPlatformProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AndroidPlatformProperties, AndroidPlatformInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AndroidPlatform"
    return model
    

AndroidPlatform = create_schema_org_model()