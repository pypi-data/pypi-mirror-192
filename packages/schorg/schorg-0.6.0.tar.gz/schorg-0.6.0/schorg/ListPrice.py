"""
Represents the list price (the price a product is actually advertised for) of an offered product.

https://schema.org/ListPrice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ListPriceInheritedProperties(TypedDict):
    """Represents the list price (the price a product is actually advertised for) of an offered product.

    References:
        https://schema.org/ListPrice
    Note:
        Model Depth 5
    Attributes:
    """

    


class ListPriceProperties(TypedDict):
    """Represents the list price (the price a product is actually advertised for) of an offered product.

    References:
        https://schema.org/ListPrice
    Note:
        Model Depth 5
    Attributes:
    """

    

#ListPriceInheritedPropertiesTd = ListPriceInheritedProperties()
#ListPricePropertiesTd = ListPriceProperties()


class AllProperties(ListPriceInheritedProperties , ListPriceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ListPriceProperties, ListPriceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ListPrice"
    return model
    

ListPrice = create_schema_org_model()