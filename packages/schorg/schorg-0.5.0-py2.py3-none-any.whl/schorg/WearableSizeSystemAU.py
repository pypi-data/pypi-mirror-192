"""
Australian size system for wearables.

https://schema.org/WearableSizeSystemAU
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemAUInheritedProperties(TypedDict):
    """Australian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemAU
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemAUProperties(TypedDict):
    """Australian size system for wearables.

    References:
        https://schema.org/WearableSizeSystemAU
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemAUInheritedPropertiesTd = WearableSizeSystemAUInheritedProperties()
#WearableSizeSystemAUPropertiesTd = WearableSizeSystemAUProperties()


class AllProperties(WearableSizeSystemAUInheritedProperties , WearableSizeSystemAUProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemAUProperties, WearableSizeSystemAUInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemAU"
    return model
    

WearableSizeSystemAU = create_schema_org_model()