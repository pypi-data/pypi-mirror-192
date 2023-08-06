"""
Represents the downpayment (up-front payment) price component of the total price for an offered product that has additional installment payments.

https://schema.org/Downpayment
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DownpaymentInheritedProperties(TypedDict):
    """Represents the downpayment (up-front payment) price component of the total price for an offered product that has additional installment payments.

    References:
        https://schema.org/Downpayment
    Note:
        Model Depth 5
    Attributes:
    """

    


class DownpaymentProperties(TypedDict):
    """Represents the downpayment (up-front payment) price component of the total price for an offered product that has additional installment payments.

    References:
        https://schema.org/Downpayment
    Note:
        Model Depth 5
    Attributes:
    """

    

#DownpaymentInheritedPropertiesTd = DownpaymentInheritedProperties()
#DownpaymentPropertiesTd = DownpaymentProperties()


class AllProperties(DownpaymentInheritedProperties , DownpaymentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DownpaymentProperties, DownpaymentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Downpayment"
    return model
    

Downpayment = create_schema_org_model()