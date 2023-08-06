"""
An ItemList ordered with no explicit order.

https://schema.org/ItemListUnordered
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ItemListUnorderedInheritedProperties(TypedDict):
    """An ItemList ordered with no explicit order.

    References:
        https://schema.org/ItemListUnordered
    Note:
        Model Depth 5
    Attributes:
    """

    


class ItemListUnorderedProperties(TypedDict):
    """An ItemList ordered with no explicit order.

    References:
        https://schema.org/ItemListUnordered
    Note:
        Model Depth 5
    Attributes:
    """

    

#ItemListUnorderedInheritedPropertiesTd = ItemListUnorderedInheritedProperties()
#ItemListUnorderedPropertiesTd = ItemListUnorderedProperties()


class AllProperties(ItemListUnorderedInheritedProperties , ItemListUnorderedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ItemListUnorderedProperties, ItemListUnorderedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ItemListUnordered"
    return model
    

ItemListUnordered = create_schema_org_model()