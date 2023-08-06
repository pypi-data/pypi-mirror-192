"""
The payment has been received and processed.

https://schema.org/PaymentComplete
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentCompleteInheritedProperties(TypedDict):
    """The payment has been received and processed.

    References:
        https://schema.org/PaymentComplete
    Note:
        Model Depth 6
    Attributes:
    """

    


class PaymentCompleteProperties(TypedDict):
    """The payment has been received and processed.

    References:
        https://schema.org/PaymentComplete
    Note:
        Model Depth 6
    Attributes:
    """

    

#PaymentCompleteInheritedPropertiesTd = PaymentCompleteInheritedProperties()
#PaymentCompletePropertiesTd = PaymentCompleteProperties()


class AllProperties(PaymentCompleteInheritedProperties , PaymentCompleteProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentCompleteProperties, PaymentCompleteInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentComplete"
    return model
    

PaymentComplete = create_schema_org_model()