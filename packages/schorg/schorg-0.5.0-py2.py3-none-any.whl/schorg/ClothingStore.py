"""
A clothing store.

https://schema.org/ClothingStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ClothingStoreInheritedProperties(TypedDict):
    """A clothing store.

    References:
        https://schema.org/ClothingStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ClothingStoreProperties(TypedDict):
    """A clothing store.

    References:
        https://schema.org/ClothingStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ClothingStoreInheritedPropertiesTd = ClothingStoreInheritedProperties()
#ClothingStorePropertiesTd = ClothingStoreProperties()


class AllProperties(ClothingStoreInheritedProperties , ClothingStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ClothingStoreProperties, ClothingStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ClothingStore"
    return model
    

ClothingStore = create_schema_org_model()