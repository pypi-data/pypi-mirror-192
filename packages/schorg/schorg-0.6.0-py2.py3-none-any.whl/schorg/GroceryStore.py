"""
A grocery store.

https://schema.org/GroceryStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GroceryStoreInheritedProperties(TypedDict):
    """A grocery store.

    References:
        https://schema.org/GroceryStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class GroceryStoreProperties(TypedDict):
    """A grocery store.

    References:
        https://schema.org/GroceryStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#GroceryStoreInheritedPropertiesTd = GroceryStoreInheritedProperties()
#GroceryStorePropertiesTd = GroceryStoreProperties()


class AllProperties(GroceryStoreInheritedProperties , GroceryStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GroceryStoreProperties, GroceryStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GroceryStore"
    return model
    

GroceryStore = create_schema_org_model()