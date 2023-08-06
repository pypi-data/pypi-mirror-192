"""
Size group "Short" for wearables.

https://schema.org/WearableSizeGroupShort
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupShortInheritedProperties(TypedDict):
    """Size group "Short" for wearables.

    References:
        https://schema.org/WearableSizeGroupShort
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupShortProperties(TypedDict):
    """Size group "Short" for wearables.

    References:
        https://schema.org/WearableSizeGroupShort
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupShortInheritedPropertiesTd = WearableSizeGroupShortInheritedProperties()
#WearableSizeGroupShortPropertiesTd = WearableSizeGroupShortProperties()


class AllProperties(WearableSizeGroupShortInheritedProperties , WearableSizeGroupShortProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupShortProperties, WearableSizeGroupShortInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupShort"
    return model
    

WearableSizeGroupShort = create_schema_org_model()