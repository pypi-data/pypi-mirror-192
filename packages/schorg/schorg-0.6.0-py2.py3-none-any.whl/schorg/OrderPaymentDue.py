"""
OrderStatus representing that payment is due on an order.

https://schema.org/OrderPaymentDue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderPaymentDueInheritedProperties(TypedDict):
    """OrderStatus representing that payment is due on an order.

    References:
        https://schema.org/OrderPaymentDue
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderPaymentDueProperties(TypedDict):
    """OrderStatus representing that payment is due on an order.

    References:
        https://schema.org/OrderPaymentDue
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderPaymentDueInheritedPropertiesTd = OrderPaymentDueInheritedProperties()
#OrderPaymentDuePropertiesTd = OrderPaymentDueProperties()


class AllProperties(OrderPaymentDueInheritedProperties , OrderPaymentDueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderPaymentDueProperties, OrderPaymentDueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderPaymentDue"
    return model
    

OrderPaymentDue = create_schema_org_model()