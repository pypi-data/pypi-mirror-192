"""
Size group "Extra Tall" for wearables.

https://schema.org/WearableSizeGroupExtraTall
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupExtraTallInheritedProperties(TypedDict):
    """Size group "Extra Tall" for wearables.

    References:
        https://schema.org/WearableSizeGroupExtraTall
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupExtraTallProperties(TypedDict):
    """Size group "Extra Tall" for wearables.

    References:
        https://schema.org/WearableSizeGroupExtraTall
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupExtraTallInheritedPropertiesTd = WearableSizeGroupExtraTallInheritedProperties()
#WearableSizeGroupExtraTallPropertiesTd = WearableSizeGroupExtraTallProperties()


class AllProperties(WearableSizeGroupExtraTallInheritedProperties , WearableSizeGroupExtraTallProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupExtraTallProperties, WearableSizeGroupExtraTallInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupExtraTall"
    return model
    

WearableSizeGroupExtraTall = create_schema_org_model()