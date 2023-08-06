"""
Represents the broad notion of 'desktop' browsers as a Web Platform.

https://schema.org/DesktopWebPlatform
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DesktopWebPlatformInheritedProperties(TypedDict):
    """Represents the broad notion of 'desktop' browsers as a Web Platform.

    References:
        https://schema.org/DesktopWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    


class DesktopWebPlatformProperties(TypedDict):
    """Represents the broad notion of 'desktop' browsers as a Web Platform.

    References:
        https://schema.org/DesktopWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    

#DesktopWebPlatformInheritedPropertiesTd = DesktopWebPlatformInheritedProperties()
#DesktopWebPlatformPropertiesTd = DesktopWebPlatformProperties()


class AllProperties(DesktopWebPlatformInheritedProperties , DesktopWebPlatformProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DesktopWebPlatformProperties, DesktopWebPlatformInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DesktopWebPlatform"
    return model
    

DesktopWebPlatform = create_schema_org_model()