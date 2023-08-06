"""
An ItemList ordered with lower values listed first.

https://schema.org/ItemListOrderAscending
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ItemListOrderAscendingInheritedProperties(TypedDict):
    """An ItemList ordered with lower values listed first.

    References:
        https://schema.org/ItemListOrderAscending
    Note:
        Model Depth 5
    Attributes:
    """

    


class ItemListOrderAscendingProperties(TypedDict):
    """An ItemList ordered with lower values listed first.

    References:
        https://schema.org/ItemListOrderAscending
    Note:
        Model Depth 5
    Attributes:
    """

    

#ItemListOrderAscendingInheritedPropertiesTd = ItemListOrderAscendingInheritedProperties()
#ItemListOrderAscendingPropertiesTd = ItemListOrderAscendingProperties()


class AllProperties(ItemListOrderAscendingInheritedProperties , ItemListOrderAscendingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ItemListOrderAscendingProperties, ItemListOrderAscendingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ItemListOrderAscending"
    return model
    

ItemListOrderAscending = create_schema_org_model()