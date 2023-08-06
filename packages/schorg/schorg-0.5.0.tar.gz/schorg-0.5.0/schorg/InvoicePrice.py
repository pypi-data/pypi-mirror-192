"""
Represents the invoice price of an offered product.

https://schema.org/InvoicePrice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InvoicePriceInheritedProperties(TypedDict):
    """Represents the invoice price of an offered product.

    References:
        https://schema.org/InvoicePrice
    Note:
        Model Depth 5
    Attributes:
    """

    


class InvoicePriceProperties(TypedDict):
    """Represents the invoice price of an offered product.

    References:
        https://schema.org/InvoicePrice
    Note:
        Model Depth 5
    Attributes:
    """

    

#InvoicePriceInheritedPropertiesTd = InvoicePriceInheritedProperties()
#InvoicePricePropertiesTd = InvoicePriceProperties()


class AllProperties(InvoicePriceInheritedProperties , InvoicePriceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InvoicePriceProperties, InvoicePriceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InvoicePrice"
    return model
    

InvoicePrice = create_schema_org_model()