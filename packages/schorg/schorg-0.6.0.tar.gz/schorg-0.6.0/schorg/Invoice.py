"""
A statement of the money due for goods or services; a bill.

https://schema.org/Invoice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InvoiceInheritedProperties(TypedDict):
    """A statement of the money due for goods or services; a bill.

    References:
        https://schema.org/Invoice
    Note:
        Model Depth 3
    Attributes:
    """

    


class InvoiceProperties(TypedDict):
    """A statement of the money due for goods or services; a bill.

    References:
        https://schema.org/Invoice
    Note:
        Model Depth 3
    Attributes:
        confirmationNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A number that confirms the given order or payment has been received.
        broker: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An entity that arranges for an exchange between a buyer and a seller.  In most cases a broker never acquires or releases ownership of a product or service involved in an exchange.  If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms are preferred.
        paymentDueDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The date that payment is due.
        provider: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The service provider, service operator, or service performer; the goods producer. Another party (a seller) may offer those services or goods on behalf of the provider. A provider may also serve as the seller.
        totalPaymentDue: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The total amount due.
        accountId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The identifier for the account the payment will be applied to.
        customer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Party placing the order or paying the invoice.
        paymentDue: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The date that payment is due.
        billingPeriod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The time interval used to compute the invoice.
        paymentMethodId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An identifier for the method of payment used (e.g. the last 4 digits of the credit card).
        paymentStatus: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The status of payment; whether the invoice has been paid or not.
        paymentMethod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The name of the credit card or other method of payment for the order.
        scheduledPaymentDate: (Optional[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]): The date the invoice is scheduled to be paid.
        referencesOrder: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The Order(s) related to this Invoice. One or more Orders may be combined into a single Invoice.
        category: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A category for the item. Greater signs or slashes can be used to informally indicate a category hierarchy.
        minimumPaymentDue: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The minimum payment required at this time.
    """

    confirmationNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    broker: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentDueDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    provider: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    totalPaymentDue: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    accountId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    customer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentDue: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    billingPeriod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentMethodId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    paymentStatus: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    paymentMethod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    scheduledPaymentDate: NotRequired[Union[List[Union[SchemaOrgObj, str, date]], SchemaOrgObj, str, date]]
    referencesOrder: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    category: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    minimumPaymentDue: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#InvoiceInheritedPropertiesTd = InvoiceInheritedProperties()
#InvoicePropertiesTd = InvoiceProperties()


class AllProperties(InvoiceInheritedProperties , InvoiceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InvoiceProperties, InvoiceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Invoice"
    return model
    

Invoice = create_schema_org_model()