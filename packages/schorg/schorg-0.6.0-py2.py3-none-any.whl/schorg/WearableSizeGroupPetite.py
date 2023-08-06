"""
Size group "Petite" for wearables.

https://schema.org/WearableSizeGroupPetite
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupPetiteInheritedProperties(TypedDict):
    """Size group "Petite" for wearables.

    References:
        https://schema.org/WearableSizeGroupPetite
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupPetiteProperties(TypedDict):
    """Size group "Petite" for wearables.

    References:
        https://schema.org/WearableSizeGroupPetite
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupPetiteInheritedPropertiesTd = WearableSizeGroupPetiteInheritedProperties()
#WearableSizeGroupPetitePropertiesTd = WearableSizeGroupPetiteProperties()


class AllProperties(WearableSizeGroupPetiteInheritedProperties , WearableSizeGroupPetiteProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupPetiteProperties, WearableSizeGroupPetiteInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupPetite"
    return model
    

WearableSizeGroupPetite = create_schema_org_model()