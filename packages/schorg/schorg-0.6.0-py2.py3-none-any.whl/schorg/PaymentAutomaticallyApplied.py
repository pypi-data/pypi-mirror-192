"""
An automatic payment system is in place and will be used.

https://schema.org/PaymentAutomaticallyApplied
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentAutomaticallyAppliedInheritedProperties(TypedDict):
    """An automatic payment system is in place and will be used.

    References:
        https://schema.org/PaymentAutomaticallyApplied
    Note:
        Model Depth 6
    Attributes:
    """

    


class PaymentAutomaticallyAppliedProperties(TypedDict):
    """An automatic payment system is in place and will be used.

    References:
        https://schema.org/PaymentAutomaticallyApplied
    Note:
        Model Depth 6
    Attributes:
    """

    

#PaymentAutomaticallyAppliedInheritedPropertiesTd = PaymentAutomaticallyAppliedInheritedProperties()
#PaymentAutomaticallyAppliedPropertiesTd = PaymentAutomaticallyAppliedProperties()


class AllProperties(PaymentAutomaticallyAppliedInheritedProperties , PaymentAutomaticallyAppliedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentAutomaticallyAppliedProperties, PaymentAutomaticallyAppliedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentAutomaticallyApplied"
    return model
    

PaymentAutomaticallyApplied = create_schema_org_model()