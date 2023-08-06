"""
OrderStatus representing that an order is being processed.

https://schema.org/OrderProcessing
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderProcessingInheritedProperties(TypedDict):
    """OrderStatus representing that an order is being processed.

    References:
        https://schema.org/OrderProcessing
    Note:
        Model Depth 6
    Attributes:
    """

    


class OrderProcessingProperties(TypedDict):
    """OrderStatus representing that an order is being processed.

    References:
        https://schema.org/OrderProcessing
    Note:
        Model Depth 6
    Attributes:
    """

    

#OrderProcessingInheritedPropertiesTd = OrderProcessingInheritedProperties()
#OrderProcessingPropertiesTd = OrderProcessingProperties()


class AllProperties(OrderProcessingInheritedProperties , OrderProcessingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderProcessingProperties, OrderProcessingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OrderProcessing"
    return model
    

OrderProcessing = create_schema_org_model()