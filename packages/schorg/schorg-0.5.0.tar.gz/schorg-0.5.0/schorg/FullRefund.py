"""
Specifies that a refund can be done in the full amount the customer paid for the product.

https://schema.org/FullRefund
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FullRefundInheritedProperties(TypedDict):
    """Specifies that a refund can be done in the full amount the customer paid for the product.

    References:
        https://schema.org/FullRefund
    Note:
        Model Depth 5
    Attributes:
    """

    


class FullRefundProperties(TypedDict):
    """Specifies that a refund can be done in the full amount the customer paid for the product.

    References:
        https://schema.org/FullRefund
    Note:
        Model Depth 5
    Attributes:
    """

    

#FullRefundInheritedPropertiesTd = FullRefundInheritedProperties()
#FullRefundPropertiesTd = FullRefundProperties()


class AllProperties(FullRefundInheritedProperties , FullRefundProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FullRefundProperties, FullRefundInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FullRefund"
    return model
    

FullRefund = create_schema_org_model()