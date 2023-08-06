"""
A payment method is a standardized procedure for transferring the monetary amount for a purchase. Payment methods are characterized by the legal and technical structures used, and by the organization or group carrying out the transaction.Commonly used values:* http://purl.org/goodrelations/v1#ByBankTransferInAdvance* http://purl.org/goodrelations/v1#ByInvoice* http://purl.org/goodrelations/v1#Cash* http://purl.org/goodrelations/v1#CheckInAdvance* http://purl.org/goodrelations/v1#COD* http://purl.org/goodrelations/v1#DirectDebit* http://purl.org/goodrelations/v1#GoogleCheckout* http://purl.org/goodrelations/v1#PayPal* http://purl.org/goodrelations/v1#PaySwarm        

https://schema.org/PaymentMethod
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaymentMethodInheritedProperties(TypedDict):
    """A payment method is a standardized procedure for transferring the monetary amount for a purchase. Payment methods are characterized by the legal and technical structures used, and by the organization or group carrying out the transaction.Commonly used values:* http://purl.org/goodrelations/v1#ByBankTransferInAdvance* http://purl.org/goodrelations/v1#ByInvoice* http://purl.org/goodrelations/v1#Cash* http://purl.org/goodrelations/v1#CheckInAdvance* http://purl.org/goodrelations/v1#COD* http://purl.org/goodrelations/v1#DirectDebit* http://purl.org/goodrelations/v1#GoogleCheckout* http://purl.org/goodrelations/v1#PayPal* http://purl.org/goodrelations/v1#PaySwarm        

    References:
        https://schema.org/PaymentMethod
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PaymentMethodProperties(TypedDict):
    """A payment method is a standardized procedure for transferring the monetary amount for a purchase. Payment methods are characterized by the legal and technical structures used, and by the organization or group carrying out the transaction.Commonly used values:* http://purl.org/goodrelations/v1#ByBankTransferInAdvance* http://purl.org/goodrelations/v1#ByInvoice* http://purl.org/goodrelations/v1#Cash* http://purl.org/goodrelations/v1#CheckInAdvance* http://purl.org/goodrelations/v1#COD* http://purl.org/goodrelations/v1#DirectDebit* http://purl.org/goodrelations/v1#GoogleCheckout* http://purl.org/goodrelations/v1#PayPal* http://purl.org/goodrelations/v1#PaySwarm        

    References:
        https://schema.org/PaymentMethod
    Note:
        Model Depth 4
    Attributes:
    """

    

#PaymentMethodInheritedPropertiesTd = PaymentMethodInheritedProperties()
#PaymentMethodPropertiesTd = PaymentMethodProperties()


class AllProperties(PaymentMethodInheritedProperties , PaymentMethodProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaymentMethodProperties, PaymentMethodInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaymentMethod"
    return model
    

PaymentMethod = create_schema_org_model()