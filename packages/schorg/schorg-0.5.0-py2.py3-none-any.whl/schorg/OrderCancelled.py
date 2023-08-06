"""
OrderStatus representing cancellation of an order.

https://schema.org/OrderCancelled
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderCancelledInheritedProperties(TypedDict):
    """OrderStatus representing cancellation of an order.

    References:
        https://schema.org/OrderCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderCancelledProperties(TypedDict):
    """OrderStatus representing cancellation of an order.

    References:
        https://schema.org/OrderCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderCancelledInheritedPropertiesTd = OrderCancelledInheritedProperties()
#OrderCancelledPropertiesTd = OrderCancelledProperties()


class AllProperties(OrderCancelledInheritedProperties , OrderCancelledProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderCancelledProperties, OrderCancelledInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderCancelled"
    return model
    

OrderCancelled = create_schema_org_model()