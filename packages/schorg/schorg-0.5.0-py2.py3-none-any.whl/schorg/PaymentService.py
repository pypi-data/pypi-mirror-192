"""
A Service to transfer funds from a person or organization to a beneficiary person or organization.

https://schema.org/PaymentService
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentServiceInheritedProperties(TypedDict):
    """A Service to transfer funds from a person or organization to a beneficiary person or organization.

    References:
        https://schema.org/PaymentService
    Note:
        Model Depth 5
    Attributes:
        annualPercentageRate: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The annual rate that is charged for borrowing (or made by investing), expressed as a single percentage number that represents the actual yearly cost of funds over the term of a loan. This includes any fees or additional costs associated with the transaction.
        interestRate: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The interest rate, charged or paid, applicable to the financial product. Note: This is different from the calculated annualPercentageRate.
        feesAndCommissionsSpecification: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): Description of fees, commissions, and other terms applied either to a class of financial product, or by a financial service organization.
    """

    annualPercentageRate: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    interestRate: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    feesAndCommissionsSpecification: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class PaymentServiceProperties(TypedDict):
    """A Service to transfer funds from a person or organization to a beneficiary person or organization.

    References:
        https://schema.org/PaymentService
    Note:
        Model Depth 5
    Attributes:
    """

    

#PaymentServiceInheritedPropertiesTd = PaymentServiceInheritedProperties()
#PaymentServicePropertiesTd = PaymentServiceProperties()


class AllProperties(PaymentServiceInheritedProperties , PaymentServiceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentServiceProperties, PaymentServiceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentService"
    return model
    

PaymentService = create_schema_org_model()