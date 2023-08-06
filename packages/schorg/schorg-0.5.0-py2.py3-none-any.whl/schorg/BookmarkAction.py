"""
An agent bookmarks/flags/labels/tags/marks an object.

https://schema.org/BookmarkAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BookmarkActionInheritedProperties(TypedDict):
    """An agent bookmarks/flags/labels/tags/marks an object.

    References:
        https://schema.org/BookmarkAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class BookmarkActionProperties(TypedDict):
    """An agent bookmarks/flags/labels/tags/marks an object.

    References:
        https://schema.org/BookmarkAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#BookmarkActionInheritedPropertiesTd = BookmarkActionInheritedProperties()
#BookmarkActionPropertiesTd = BookmarkActionProperties()


class AllProperties(BookmarkActionInheritedProperties , BookmarkActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BookmarkActionProperties, BookmarkActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BookmarkAction"
    return model
    

BookmarkAction = create_schema_org_model()