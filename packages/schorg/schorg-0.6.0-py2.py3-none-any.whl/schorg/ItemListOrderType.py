"""
Enumerated for values for itemListOrder for indicating how an ordered ItemList is organized.

https://schema.org/ItemListOrderType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ItemListOrderTypeInheritedProperties(TypedDict):
    """Enumerated for values for itemListOrder for indicating how an ordered ItemList is organized.

    References:
        https://schema.org/ItemListOrderType
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class ItemListOrderTypeProperties(TypedDict):
    """Enumerated for values for itemListOrder for indicating how an ordered ItemList is organized.

    References:
        https://schema.org/ItemListOrderType
    Note:
        Model Depth 4
    Attributes:
    """

    

#ItemListOrderTypeInheritedPropertiesTd = ItemListOrderTypeInheritedProperties()
#ItemListOrderTypePropertiesTd = ItemListOrderTypeProperties()


class AllProperties(ItemListOrderTypeInheritedProperties , ItemListOrderTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ItemListOrderTypeProperties, ItemListOrderTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ItemListOrderType"
    return model
    

ItemListOrderType = create_schema_org_model()