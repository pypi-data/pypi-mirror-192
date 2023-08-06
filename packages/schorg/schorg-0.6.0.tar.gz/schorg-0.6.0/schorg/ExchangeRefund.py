"""
Specifies that a refund can be done as an exchange for the same product.

https://schema.org/ExchangeRefund
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ExchangeRefundInheritedProperties(TypedDict):
    """Specifies that a refund can be done as an exchange for the same product.

    References:
        https://schema.org/ExchangeRefund
    Note:
        Model Depth 5
    Attributes:
    """

    


class ExchangeRefundProperties(TypedDict):
    """Specifies that a refund can be done as an exchange for the same product.

    References:
        https://schema.org/ExchangeRefund
    Note:
        Model Depth 5
    Attributes:
    """

    

#ExchangeRefundInheritedPropertiesTd = ExchangeRefundInheritedProperties()
#ExchangeRefundPropertiesTd = ExchangeRefundProperties()


class AllProperties(ExchangeRefundInheritedProperties , ExchangeRefundProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ExchangeRefundProperties, ExchangeRefundInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ExchangeRefund"
    return model
    

ExchangeRefund = create_schema_org_model()