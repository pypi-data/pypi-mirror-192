"""
A bookstore.

https://schema.org/BookStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BookStoreInheritedProperties(TypedDict):
    """A bookstore.

    References:
        https://schema.org/BookStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class BookStoreProperties(TypedDict):
    """A bookstore.

    References:
        https://schema.org/BookStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#BookStoreInheritedPropertiesTd = BookStoreInheritedProperties()
#BookStorePropertiesTd = BookStoreProperties()


class AllProperties(BookStoreInheritedProperties , BookStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BookStoreProperties, BookStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BookStore"
    return model
    

BookStore = create_schema_org_model()