"""
Indicates that the item is in stock.

https://schema.org/InStock
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InStockInheritedProperties(TypedDict):
    """Indicates that the item is in stock.

    References:
        https://schema.org/InStock
    Note:
        Model Depth 5
    Attributes:
    """

    


class InStockProperties(TypedDict):
    """Indicates that the item is in stock.

    References:
        https://schema.org/InStock
    Note:
        Model Depth 5
    Attributes:
    """

    

#InStockInheritedPropertiesTd = InStockInheritedProperties()
#InStockPropertiesTd = InStockProperties()


class AllProperties(InStockInheritedProperties , InStockProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InStockProperties, InStockInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InStock"
    return model
    

InStock = create_schema_org_model()