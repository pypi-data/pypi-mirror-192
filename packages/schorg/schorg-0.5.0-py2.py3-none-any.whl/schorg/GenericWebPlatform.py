"""
Represents the generic notion of the Web Platform. More specific codes include [[MobileWebPlatform]] and [[DesktopWebPlatform]], as an incomplete list. 

https://schema.org/GenericWebPlatform
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GenericWebPlatformInheritedProperties(TypedDict):
    """Represents the generic notion of the Web Platform. More specific codes include [[MobileWebPlatform]] and [[DesktopWebPlatform]], as an incomplete list. 

    References:
        https://schema.org/GenericWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    


class GenericWebPlatformProperties(TypedDict):
    """Represents the generic notion of the Web Platform. More specific codes include [[MobileWebPlatform]] and [[DesktopWebPlatform]], as an incomplete list. 

    References:
        https://schema.org/GenericWebPlatform
    Note:
        Model Depth 5
    Attributes:
    """

    

#GenericWebPlatformInheritedPropertiesTd = GenericWebPlatformInheritedProperties()
#GenericWebPlatformPropertiesTd = GenericWebPlatformProperties()


class AllProperties(GenericWebPlatformInheritedProperties , GenericWebPlatformProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GenericWebPlatformProperties, GenericWebPlatformInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GenericWebPlatform"
    return model
    

GenericWebPlatform = create_schema_org_model()