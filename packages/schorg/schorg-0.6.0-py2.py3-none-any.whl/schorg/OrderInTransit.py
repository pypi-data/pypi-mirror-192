"""
OrderStatus representing that an order is in transit.

https://schema.org/OrderInTransit
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderInTransitInheritedProperties(TypedDict):
    """OrderStatus representing that an order is in transit.

    References:
        https://schema.org/OrderInTransit
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderInTransitProperties(TypedDict):
    """OrderStatus representing that an order is in transit.

    References:
        https://schema.org/OrderInTransit
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderInTransitInheritedPropertiesTd = OrderInTransitInheritedProperties()
#OrderInTransitPropertiesTd = OrderInTransitProperties()


class AllProperties(OrderInTransitInheritedProperties , OrderInTransitProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderInTransitProperties, OrderInTransitInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderInTransit"
    return model
    

OrderInTransit = create_schema_org_model()