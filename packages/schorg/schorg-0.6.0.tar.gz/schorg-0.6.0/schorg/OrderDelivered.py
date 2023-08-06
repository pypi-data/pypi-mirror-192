"""
OrderStatus representing successful delivery of an order.

https://schema.org/OrderDelivered
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderDeliveredInheritedProperties(TypedDict):
    """OrderStatus representing successful delivery of an order.

    References:
        https://schema.org/OrderDelivered
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderDeliveredProperties(TypedDict):
    """OrderStatus representing successful delivery of an order.

    References:
        https://schema.org/OrderDelivered
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderDeliveredInheritedPropertiesTd = OrderDeliveredInheritedProperties()
#OrderDeliveredPropertiesTd = OrderDeliveredProperties()


class AllProperties(OrderDeliveredInheritedProperties , OrderDeliveredProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderDeliveredProperties, OrderDeliveredInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderDelivered"
    return model
    

OrderDelivered = create_schema_org_model()