"""
Size group "Big" for wearables.

https://schema.org/WearableSizeGroupBig
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupBigInheritedProperties(TypedDict):
    """Size group "Big" for wearables.

    References:
        https://schema.org/WearableSizeGroupBig
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupBigProperties(TypedDict):
    """Size group "Big" for wearables.

    References:
        https://schema.org/WearableSizeGroupBig
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupBigInheritedPropertiesTd = WearableSizeGroupBigInheritedProperties()
#WearableSizeGroupBigPropertiesTd = WearableSizeGroupBigProperties()


class AllProperties(WearableSizeGroupBigInheritedProperties , WearableSizeGroupBigProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupBigProperties, WearableSizeGroupBigInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupBig"
    return model
    

WearableSizeGroupBig = create_schema_org_model()