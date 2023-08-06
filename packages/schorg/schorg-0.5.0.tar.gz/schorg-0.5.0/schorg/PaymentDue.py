"""
The payment is due, but still within an acceptable time to be received.

https://schema.org/PaymentDue
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentDueInheritedProperties(TypedDict):
    """The payment is due, but still within an acceptable time to be received.

    References:
        https://schema.org/PaymentDue
    Note:
        Model Depth 6
    Attributes:
    """

    


class PaymentDueProperties(TypedDict):
    """The payment is due, but still within an acceptable time to be received.

    References:
        https://schema.org/PaymentDue
    Note:
        Model Depth 6
    Attributes:
    """

    

#PaymentDueInheritedPropertiesTd = PaymentDueInheritedProperties()
#PaymentDuePropertiesTd = PaymentDueProperties()


class AllProperties(PaymentDueInheritedProperties , PaymentDueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentDueProperties, PaymentDueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentDue"
    return model
    

PaymentDue = create_schema_org_model()