"""
An list item, e.g. a step in a checklist or how-to description.

https://schema.org/ListItem
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ListItemInheritedProperties(TypedDict):
    """An list item, e.g. a step in a checklist or how-to description.

    References:
        https://schema.org/ListItem
    Note:
        Model Depth 3
    Attributes:
    """

    


class ListItemProperties(TypedDict):
    """An list item, e.g. a step in a checklist or how-to description.

    References:
        https://schema.org/ListItem
    Note:
        Model Depth 3
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
    

#ListItemInheritedPropertiesTd = ListItemInheritedProperties()
#ListItemPropertiesTd = ListItemProperties()


class AllProperties(ListItemInheritedProperties , ListItemProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ListItemProperties, ListItemInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ListItem"
    return model
    

ListItem = create_schema_org_model()