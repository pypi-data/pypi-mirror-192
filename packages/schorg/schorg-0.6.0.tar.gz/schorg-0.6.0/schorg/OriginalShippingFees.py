"""
Specifies that the customer must pay the original shipping costs when returning a product.

https://schema.org/OriginalShippingFees
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OriginalShippingFeesInheritedProperties(TypedDict):
    """Specifies that the customer must pay the original shipping costs when returning a product.

    References:
        https://schema.org/OriginalShippingFees
    Note:
        Model Depth 5
    Attributes:
    """

    


class OriginalShippingFeesProperties(TypedDict):
    """Specifies that the customer must pay the original shipping costs when returning a product.

    References:
        https://schema.org/OriginalShippingFees
    Note:
        Model Depth 5
    Attributes:
    """

    

#OriginalShippingFeesInheritedPropertiesTd = OriginalShippingFeesInheritedProperties()
#OriginalShippingFeesPropertiesTd = OriginalShippingFeesProperties()


class AllProperties(OriginalShippingFeesInheritedProperties , OriginalShippingFeesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OriginalShippingFeesProperties, OriginalShippingFeesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OriginalShippingFees"
    return model
    

OriginalShippingFees = create_schema_org_model()