"""
A furniture store.

https://schema.org/FurnitureStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FurnitureStoreInheritedProperties(TypedDict):
    """A furniture store.

    References:
        https://schema.org/FurnitureStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class FurnitureStoreProperties(TypedDict):
    """A furniture store.

    References:
        https://schema.org/FurnitureStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#FurnitureStoreInheritedPropertiesTd = FurnitureStoreInheritedProperties()
#FurnitureStorePropertiesTd = FurnitureStoreProperties()


class AllProperties(FurnitureStoreInheritedProperties , FurnitureStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FurnitureStoreProperties, FurnitureStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FurnitureStore"
    return model
    

FurnitureStore = create_schema_org_model()