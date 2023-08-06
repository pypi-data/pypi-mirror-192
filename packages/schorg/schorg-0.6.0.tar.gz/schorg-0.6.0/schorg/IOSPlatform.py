"""
Represents the broad notion of iOS-based operating systems.

https://schema.org/IOSPlatform
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class IOSPlatformInheritedProperties(TypedDict):
    """Represents the broad notion of iOS-based operating systems.

    References:
        https://schema.org/IOSPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    


class IOSPlatformProperties(TypedDict):
    """Represents the broad notion of iOS-based operating systems.

    References:
        https://schema.org/IOSPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    

#IOSPlatformInheritedPropertiesTd = IOSPlatformInheritedProperties()
#IOSPlatformPropertiesTd = IOSPlatformProperties()


class AllProperties(IOSPlatformInheritedProperties , IOSPlatformProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[IOSPlatformProperties, IOSPlatformInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "IOSPlatform"
    return model
    

IOSPlatform = create_schema_org_model()