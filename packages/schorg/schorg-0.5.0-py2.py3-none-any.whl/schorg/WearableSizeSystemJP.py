"""
Japanese size system for wearables.

https://schema.org/WearableSizeSystemJP
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemJPInheritedProperties(TypedDict):
    """Japanese size system for wearables.

    References:
        https://schema.org/WearableSizeSystemJP
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemJPProperties(TypedDict):
    """Japanese size system for wearables.

    References:
        https://schema.org/WearableSizeSystemJP
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemJPInheritedPropertiesTd = WearableSizeSystemJPInheritedProperties()
#WearableSizeSystemJPPropertiesTd = WearableSizeSystemJPProperties()


class AllProperties(WearableSizeSystemJPInheritedProperties , WearableSizeSystemJPProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemJPProperties, WearableSizeSystemJPInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemJP"
    return model
    

WearableSizeSystemJP = create_schema_org_model()