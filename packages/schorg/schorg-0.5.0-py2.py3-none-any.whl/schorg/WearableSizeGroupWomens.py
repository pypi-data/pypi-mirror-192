"""
Size group "Womens" for wearables.

https://schema.org/WearableSizeGroupWomens
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupWomensInheritedProperties(TypedDict):
    """Size group "Womens" for wearables.

    References:
        https://schema.org/WearableSizeGroupWomens
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupWomensProperties(TypedDict):
    """Size group "Womens" for wearables.

    References:
        https://schema.org/WearableSizeGroupWomens
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupWomensInheritedPropertiesTd = WearableSizeGroupWomensInheritedProperties()
#WearableSizeGroupWomensPropertiesTd = WearableSizeGroupWomensProperties()


class AllProperties(WearableSizeGroupWomensInheritedProperties , WearableSizeGroupWomensProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupWomensProperties, WearableSizeGroupWomensInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupWomens"
    return model
    

WearableSizeGroupWomens = create_schema_org_model()