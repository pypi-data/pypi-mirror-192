"""
OrderStatus representing that an order has been returned.

https://schema.org/OrderReturned
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderReturnedInheritedProperties(TypedDict):
    """OrderStatus representing that an order has been returned.

    References:
        https://schema.org/OrderReturned
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderReturnedProperties(TypedDict):
    """OrderStatus representing that an order has been returned.

    References:
        https://schema.org/OrderReturned
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderReturnedInheritedPropertiesTd = OrderReturnedInheritedProperties()
#OrderReturnedPropertiesTd = OrderReturnedProperties()


class AllProperties(OrderReturnedInheritedProperties , OrderReturnedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderReturnedProperties, OrderReturnedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderReturned"
    return model
    

OrderReturned = create_schema_org_model()