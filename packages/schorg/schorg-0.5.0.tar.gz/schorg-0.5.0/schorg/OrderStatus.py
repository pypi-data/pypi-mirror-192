"""
Enumerated status values for Order.

https://schema.org/OrderStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderStatusInheritedProperties(TypedDict):
    """Enumerated status values for Order.

    References:
        https://schema.org/OrderStatus
    Note:
        Model Depth 5
    Attributes:
    """

    


class OrderStatusProperties(TypedDict):
    """Enumerated status values for Order.

    References:
        https://schema.org/OrderStatus
    Note:
        Model Depth 5
    Attributes:
    """

    

#OrderStatusInheritedPropertiesTd = OrderStatusInheritedProperties()
#OrderStatusPropertiesTd = OrderStatusProperties()


class AllProperties(OrderStatusInheritedProperties , OrderStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderStatusProperties, OrderStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderStatus"
    return model
    

OrderStatus = create_schema_org_model()