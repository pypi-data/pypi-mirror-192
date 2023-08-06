"""
An item used as either a tool or supply when performing the instructions for how to achieve a result.

https://schema.org/HowToItem
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HowToItemInheritedProperties(TypedDict):
    """An item used as either a tool or supply when performing the instructions for how to achieve a result.

    References:
        https://schema.org/HowToItem
    Note:
        Model Depth 4
    Attributes:
        item: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An entity represented by an entry in a list or data feed (e.g. an 'artist' in a list of 'artists').
        nextItem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A link to the ListItem that follows the current one.
        previousItem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A link to the ListItem that precedes the current one.
        position: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The position of an item in a series or sequence of items.
    """

    item: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    nextItem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    previousItem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    position: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class HowToItemProperties(TypedDict):
    """An item used as either a tool or supply when performing the instructions for how to achieve a result.

    References:
        https://schema.org/HowToItem
    Note:
        Model Depth 4
    Attributes:
        requiredQuantity: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The required quantity of the item(s).
    """

    requiredQuantity: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    

#HowToItemInheritedPropertiesTd = HowToItemInheritedProperties()
#HowToItemPropertiesTd = HowToItemProperties()


class AllProperties(HowToItemInheritedProperties , HowToItemProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HowToItemProperties, HowToItemInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "HowToItem"
    return model
    

HowToItem = create_schema_org_model()