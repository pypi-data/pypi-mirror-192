"""
Size group "Maternity" for wearables.

https://schema.org/WearableSizeGroupMaternity
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupMaternityInheritedProperties(TypedDict):
    """Size group "Maternity" for wearables.

    References:
        https://schema.org/WearableSizeGroupMaternity
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupMaternityProperties(TypedDict):
    """Size group "Maternity" for wearables.

    References:
        https://schema.org/WearableSizeGroupMaternity
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupMaternityInheritedPropertiesTd = WearableSizeGroupMaternityInheritedProperties()
#WearableSizeGroupMaternityPropertiesTd = WearableSizeGroupMaternityProperties()


class AllProperties(WearableSizeGroupMaternityInheritedProperties , WearableSizeGroupMaternityProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupMaternityProperties, WearableSizeGroupMaternityInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupMaternity"
    return model
    

WearableSizeGroupMaternity = create_schema_org_model()