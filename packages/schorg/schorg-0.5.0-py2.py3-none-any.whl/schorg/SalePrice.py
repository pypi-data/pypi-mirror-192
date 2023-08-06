"""
Represents a sale price (usually active for a limited period) of an offered product.

https://schema.org/SalePrice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SalePriceInheritedProperties(TypedDict):
    """Represents a sale price (usually active for a limited period) of an offered product.

    References:
        https://schema.org/SalePrice
    Note:
        Model Depth 5
    Attributes:
    """

    


class SalePriceProperties(TypedDict):
    """Represents a sale price (usually active for a limited period) of an offered product.

    References:
        https://schema.org/SalePrice
    Note:
        Model Depth 5
    Attributes:
    """

    

#SalePriceInheritedPropertiesTd = SalePriceInheritedProperties()
#SalePricePropertiesTd = SalePriceProperties()


class AllProperties(SalePriceInheritedProperties , SalePriceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SalePriceProperties, SalePriceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SalePrice"
    return model
    

SalePrice = create_schema_org_model()