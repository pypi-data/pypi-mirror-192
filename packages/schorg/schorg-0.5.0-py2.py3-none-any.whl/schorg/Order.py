"""
An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer.

https://schema.org/Order
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OrderInheritedProperties(TypedDict):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer.

    References:
        https://schema.org/Order
    Note:
        Model Depth 3
    Attributes:
    """

    


class OrderProperties(TypedDict):
    """An order is a confirmation of a transaction (a receipt), which can contain multiple line items, each represented by an Offer that has been accepted by the customer.

    References:
        https://schema.org/Order
    Note:
        Model Depth 3
    Attributes:
        orderStatus: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The current status of the order.
        isGift: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): Indicates whether the offer was accepted as a gift for someone other than the buyer.
        confirmationNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A number that confirms the given order or payment has been received.
        broker: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An entity that arranges for an exchange between a buyer and a seller.  In most cases a broker never acquires or releases ownership of a product or service involved in an exchange.  If it is not clear whether an entity is a broker, seller, or buyer, the latter two terms are preferred.
        paymentDueDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The date that payment is due.
        seller: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An entity which offers (sells / leases / lends / loans) the services / goods.  A seller may also be a provider.
        discount: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): Any discount applied (to an Order).
        discountCurrency: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The currency of the discount.Use standard formats: [ISO 4217 currency format](http://en.wikipedia.org/wiki/ISO_4217), e.g. "USD"; [Ticker symbol](https://en.wikipedia.org/wiki/List_of_cryptocurrencies) for cryptocurrencies, e.g. "BTC"; well known names for [Local Exchange Trading Systems](https://en.wikipedia.org/wiki/Local_exchange_trading_system) (LETS) and other currency types, e.g. "Ithaca HOUR".
        customer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Party placing the order or paying the invoice.
        paymentDue: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The date that payment is due.
        acceptedOffer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The offer(s) -- e.g., product, quantity and price combinations -- included in the order.
        paymentMethodId: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): An identifier for the method of payment used (e.g. the last 4 digits of the credit card).
        merchant: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): 'merchant' is an out-dated term for 'seller'.
        partOfInvoice: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The order is being paid as part of the referenced Invoice.
        orderNumber: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The identifier of the transaction.
        paymentMethod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The name of the credit card or other method of payment for the order.
        discountCode: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Code used to redeem a discount.
        orderDelivery: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The delivery of the parcel related to this order or order item.
        orderedItem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The item ordered.
        billingAddress: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The billing address for the order.
        paymentUrl: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The URL for sending a payment.
        orderDate: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): Date order was placed.
    """

    orderStatus: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    isGift: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    confirmationNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    broker: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentDueDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    seller: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    discount: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    discountCurrency: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    customer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentDue: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    acceptedOffer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentMethodId: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    merchant: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    partOfInvoice: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    orderNumber: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    paymentMethod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    discountCode: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    orderDelivery: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    orderedItem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    billingAddress: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    paymentUrl: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    orderDate: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    

#OrderInheritedPropertiesTd = OrderInheritedProperties()
#OrderPropertiesTd = OrderProperties()


class AllProperties(OrderInheritedProperties , OrderProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OrderProperties, OrderInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Order"
    return model
    

Order = create_schema_org_model()