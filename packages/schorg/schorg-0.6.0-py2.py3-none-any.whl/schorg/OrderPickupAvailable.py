"""
OrderStatus representing availability of an order for pickup.

https://schema.org/OrderPickupAvailable
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderPickupAvailableInheritedProperties(TypedDict):
    """OrderStatus representing availability of an order for pickup.

    References:
        https://schema.org/OrderPickupAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderPickupAvailableProperties(TypedDict):
    """OrderStatus representing availability of an order for pickup.

    References:
        https://schema.org/OrderPickupAvailable
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderPickupAvailableInheritedPropertiesTd = OrderPickupAvailableInheritedProperties()
#OrderPickupAvailablePropertiesTd = OrderPickupAvailableProperties()


class AllProperties(OrderPickupAvailableInheritedProperties , OrderPickupAvailableProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderPickupAvailableProperties, OrderPickupAvailableInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderPickupAvailable"
    return model
    

OrderPickupAvailable = create_schema_org_model()