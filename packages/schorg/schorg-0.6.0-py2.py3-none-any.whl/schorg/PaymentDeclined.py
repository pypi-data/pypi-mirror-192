"""
The payee received the payment, but it was declined for some reason.

https://schema.org/PaymentDeclined
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentDeclinedInheritedProperties(TypedDict):
    """The payee received the payment, but it was declined for some reason.

    References:
        https://schema.org/PaymentDeclined
    Note:
        Model Depth 6
    Attributes:
    """

    


class PaymentDeclinedProperties(TypedDict):
    """The payee received the payment, but it was declined for some reason.

    References:
        https://schema.org/PaymentDeclined
    Note:
        Model Depth 6
    Attributes:
    """

    

#PaymentDeclinedInheritedPropertiesTd = PaymentDeclinedInheritedProperties()
#PaymentDeclinedPropertiesTd = PaymentDeclinedProperties()


class AllProperties(PaymentDeclinedInheritedProperties , PaymentDeclinedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentDeclinedProperties, PaymentDeclinedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentDeclined"
    return model
    

PaymentDeclined = create_schema_org_model()