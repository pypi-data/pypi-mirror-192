"""
Size group "Juniors" for wearables.

https://schema.org/WearableSizeGroupJuniors
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupJuniorsInheritedProperties(TypedDict):
    """Size group "Juniors" for wearables.

    References:
        https://schema.org/WearableSizeGroupJuniors
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupJuniorsProperties(TypedDict):
    """Size group "Juniors" for wearables.

    References:
        https://schema.org/WearableSizeGroupJuniors
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupJuniorsInheritedPropertiesTd = WearableSizeGroupJuniorsInheritedProperties()
#WearableSizeGroupJuniorsPropertiesTd = WearableSizeGroupJuniorsProperties()


class AllProperties(WearableSizeGroupJuniorsInheritedProperties , WearableSizeGroupJuniorsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupJuniorsProperties, WearableSizeGroupJuniorsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupJuniors"
    return model
    

WearableSizeGroupJuniors = create_schema_org_model()