"""
United Kingdom size system for wearables.

https://schema.org/WearableSizeSystemUK
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemUKInheritedProperties(TypedDict):
    """United Kingdom size system for wearables.

    References:
        https://schema.org/WearableSizeSystemUK
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemUKProperties(TypedDict):
    """United Kingdom size system for wearables.

    References:
        https://schema.org/WearableSizeSystemUK
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemUKInheritedPropertiesTd = WearableSizeSystemUKInheritedProperties()
#WearableSizeSystemUKPropertiesTd = WearableSizeSystemUKProperties()


class AllProperties(WearableSizeSystemUKInheritedProperties , WearableSizeSystemUKProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemUKProperties, WearableSizeSystemUKInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemUK"
    return model
    

WearableSizeSystemUK = create_schema_org_model()