"""
A garden store.

https://schema.org/GardenStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GardenStoreInheritedProperties(TypedDict):
    """A garden store.

    References:
        https://schema.org/GardenStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class GardenStoreProperties(TypedDict):
    """A garden store.

    References:
        https://schema.org/GardenStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#GardenStoreInheritedPropertiesTd = GardenStoreInheritedProperties()
#GardenStorePropertiesTd = GardenStoreProperties()


class AllProperties(GardenStoreInheritedProperties , GardenStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GardenStoreProperties, GardenStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GardenStore"
    return model
    

GardenStore = create_schema_org_model()