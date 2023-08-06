"""
An ItemList ordered with higher values listed first.

https://schema.org/ItemListOrderDescending
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ItemListOrderDescendingInheritedProperties(TypedDict):
    """An ItemList ordered with higher values listed first.

    References:
        https://schema.org/ItemListOrderDescending
    Note:
        Model Depth 5
    Attributes:
    """

    


class ItemListOrderDescendingProperties(TypedDict):
    """An ItemList ordered with higher values listed first.

    References:
        https://schema.org/ItemListOrderDescending
    Note:
        Model Depth 5
    Attributes:
    """

    

#ItemListOrderDescendingInheritedPropertiesTd = ItemListOrderDescendingInheritedProperties()
#ItemListOrderDescendingPropertiesTd = ItemListOrderDescendingProperties()


class AllProperties(ItemListOrderDescendingInheritedProperties , ItemListOrderDescendingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ItemListOrderDescendingProperties, ItemListOrderDescendingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ItemListOrderDescending"
    return model
    

ItemListOrderDescending = create_schema_org_model()