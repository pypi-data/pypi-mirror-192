"""
Indicates that the item is out of stock.

https://schema.org/OutOfStock
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OutOfStockInheritedProperties(TypedDict):
    """Indicates that the item is out of stock.

    References:
        https://schema.org/OutOfStock
    Note:
        Model Depth 5
    Attributes:
    """

    


class OutOfStockProperties(TypedDict):
    """Indicates that the item is out of stock.

    References:
        https://schema.org/OutOfStock
    Note:
        Model Depth 5
    Attributes:
    """

    

#OutOfStockInheritedPropertiesTd = OutOfStockInheritedProperties()
#OutOfStockPropertiesTd = OutOfStockProperties()


class AllProperties(OutOfStockInheritedProperties , OutOfStockProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OutOfStockProperties, OutOfStockInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OutOfStock"
    return model
    

OutOfStock = create_schema_org_model()