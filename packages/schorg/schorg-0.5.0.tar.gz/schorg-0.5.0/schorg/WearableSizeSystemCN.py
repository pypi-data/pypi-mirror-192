"""
Chinese size system for wearables.

https://schema.org/WearableSizeSystemCN
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeSystemCNInheritedProperties(TypedDict):
    """Chinese size system for wearables.

    References:
        https://schema.org/WearableSizeSystemCN
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeSystemCNProperties(TypedDict):
    """Chinese size system for wearables.

    References:
        https://schema.org/WearableSizeSystemCN
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeSystemCNInheritedPropertiesTd = WearableSizeSystemCNInheritedProperties()
#WearableSizeSystemCNPropertiesTd = WearableSizeSystemCNProperties()


class AllProperties(WearableSizeSystemCNInheritedProperties , WearableSizeSystemCNProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeSystemCNProperties, WearableSizeSystemCNInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeSystemCN"
    return model
    

WearableSizeSystemCN = create_schema_org_model()