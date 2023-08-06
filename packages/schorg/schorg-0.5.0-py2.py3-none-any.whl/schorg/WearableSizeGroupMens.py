"""
Size group "Mens" for wearables.

https://schema.org/WearableSizeGroupMens
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableSizeGroupMensInheritedProperties(TypedDict):
    """Size group "Mens" for wearables.

    References:
        https://schema.org/WearableSizeGroupMens
    Note:
        Model Depth 6
    Attributes:
    """

    


class WearableSizeGroupMensProperties(TypedDict):
    """Size group "Mens" for wearables.

    References:
        https://schema.org/WearableSizeGroupMens
    Note:
        Model Depth 6
    Attributes:
    """

    

#WearableSizeGroupMensInheritedPropertiesTd = WearableSizeGroupMensInheritedProperties()
#WearableSizeGroupMensPropertiesTd = WearableSizeGroupMensProperties()


class AllProperties(WearableSizeGroupMensInheritedProperties , WearableSizeGroupMensProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableSizeGroupMensProperties, WearableSizeGroupMensInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableSizeGroupMens"
    return model
    

WearableSizeGroupMens = create_schema_org_model()