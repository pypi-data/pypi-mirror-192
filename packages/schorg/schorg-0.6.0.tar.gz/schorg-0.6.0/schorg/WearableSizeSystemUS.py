"""
United States size system for wearables.

https://schema.org/WearableSizeSystemUS
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemUSInheritedProperties(TypedDict):
    """United States size system for wearables.

    References:
        https://schema.org/WearableSizeSystemUS
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemUSProperties(TypedDict):
    """United States size system for wearables.

    References:
        https://schema.org/WearableSizeSystemUS
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemUSInheritedPropertiesTd = WearableSizeSystemUSInheritedProperties()
#WearableSizeSystemUSPropertiesTd = WearableSizeSystemUSProperties()


class AllProperties(WearableSizeSystemUSInheritedProperties , WearableSizeSystemUSProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemUSProperties, WearableSizeSystemUSInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemUS"
    return model
    

WearableSizeSystemUS = create_schema_org_model()