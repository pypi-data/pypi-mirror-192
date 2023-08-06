"""
Size group "Extra Short" for wearables.

https://schema.org/WearableSizeGroupExtraShort
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupExtraShortInheritedProperties(TypedDict):
    """Size group "Extra Short" for wearables.

    References:
        https://schema.org/WearableSizeGroupExtraShort
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupExtraShortProperties(TypedDict):
    """Size group "Extra Short" for wearables.

    References:
        https://schema.org/WearableSizeGroupExtraShort
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupExtraShortInheritedPropertiesTd = WearableSizeGroupExtraShortInheritedProperties()
#WearableSizeGroupExtraShortPropertiesTd = WearableSizeGroupExtraShortProperties()


class AllProperties(WearableSizeGroupExtraShortInheritedProperties , WearableSizeGroupExtraShortProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupExtraShortProperties, WearableSizeGroupExtraShortInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupExtraShort"
    return model
    

WearableSizeGroupExtraShort = create_schema_org_model()