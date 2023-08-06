"""
Size group "Infants" for wearables.

https://schema.org/WearableSizeGroupInfants
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupInfantsInheritedProperties(TypedDict):
    """Size group "Infants" for wearables.

    References:
        https://schema.org/WearableSizeGroupInfants
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupInfantsProperties(TypedDict):
    """Size group "Infants" for wearables.

    References:
        https://schema.org/WearableSizeGroupInfants
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupInfantsInheritedPropertiesTd = WearableSizeGroupInfantsInheritedProperties()
#WearableSizeGroupInfantsPropertiesTd = WearableSizeGroupInfantsProperties()


class AllProperties(WearableSizeGroupInfantsInheritedProperties , WearableSizeGroupInfantsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupInfantsProperties, WearableSizeGroupInfantsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupInfants"
    return model
    

WearableSizeGroupInfants = create_schema_org_model()