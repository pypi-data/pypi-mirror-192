"""
Represents the broad notion of 'mobile' browsers as a Web Platform.

https://schema.org/MobileWebPlatform
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MobileWebPlatformInheritedProperties(TypedDict):
    """Represents the broad notion of 'mobile' browsers as a Web Platform.

    References:
        https://schema.org/MobileWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    


class MobileWebPlatformProperties(TypedDict):
    """Represents the broad notion of 'mobile' browsers as a Web Platform.

    References:
        https://schema.org/MobileWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    

#MobileWebPlatformInheritedPropertiesTd = MobileWebPlatformInheritedProperties()
#MobileWebPlatformPropertiesTd = MobileWebPlatformProperties()


class AllProperties(MobileWebPlatformInheritedProperties , MobileWebPlatformProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MobileWebPlatformProperties, MobileWebPlatformInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MobileWebPlatform"
    return model
    

MobileWebPlatform = create_schema_org_model()