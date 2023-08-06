"""
The payment is due and considered late.

https://schema.org/PaymentPastDue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentPastDueInheritedProperties(TypedDict):
    """The payment is due and considered late.

    References:
        https://schema.org/PaymentPastDue
    Note:
        Model Depth 6
    Attributes:
    """

    


class PaymentPastDueProperties(TypedDict):
    """The payment is due and considered late.

    References:
        https://schema.org/PaymentPastDue
    Note:
        Model Depth 6
    Attributes:
    """

    

#PaymentPastDueInheritedPropertiesTd = PaymentPastDueInheritedProperties()
#PaymentPastDuePropertiesTd = PaymentPastDueProperties()


class AllProperties(PaymentPastDueInheritedProperties , PaymentPastDueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentPastDueProperties, PaymentPastDueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentPastDue"
    return model
    

PaymentPastDue = create_schema_org_model()