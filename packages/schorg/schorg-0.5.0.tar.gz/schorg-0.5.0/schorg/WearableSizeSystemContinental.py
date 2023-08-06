"""
Continental size system for wearables.

https://schema.org/WearableSizeSystemContinental
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemContinentalInheritedProperties(TypedDict):
    """Continental size system for wearables.

    References:
        https://schema.org/WearableSizeSystemContinental
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemContinentalProperties(TypedDict):
    """Continental size system for wearables.

    References:
        https://schema.org/WearableSizeSystemContinental
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemContinentalInheritedPropertiesTd = WearableSizeSystemContinentalInheritedProperties()
#WearableSizeSystemContinentalPropertiesTd = WearableSizeSystemContinentalProperties()


class AllProperties(WearableSizeSystemContinentalInheritedProperties , WearableSizeSystemContinentalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemContinentalProperties, WearableSizeSystemContinentalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemContinental"
    return model
    

WearableSizeSystemContinental = create_schema_org_model()