"""
Represents the minimum advertised price ("MAP") (as dictated by the manufacturer) of an offered product.

https://schema.org/MinimumAdvertisedPrice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MinimumAdvertisedPriceInheritedProperties(TypedDict):
    """Represents the minimum advertised price ("MAP") (as dictated by the manufacturer) of an offered product.

    References:
        https://schema.org/MinimumAdvertisedPrice
    Note:
        Model Depth 5
    Attributes:
    """

    


class MinimumAdvertisedPriceProperties(TypedDict):
    """Represents the minimum advertised price ("MAP") (as dictated by the manufacturer) of an offered product.

    References:
        https://schema.org/MinimumAdvertisedPrice
    Note:
        Model Depth 5
    Attributes:
    """

    

#MinimumAdvertisedPriceInheritedPropertiesTd = MinimumAdvertisedPriceInheritedProperties()
#MinimumAdvertisedPricePropertiesTd = MinimumAdvertisedPriceProperties()


class AllProperties(MinimumAdvertisedPriceInheritedProperties , MinimumAdvertisedPriceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MinimumAdvertisedPriceProperties, MinimumAdvertisedPriceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MinimumAdvertisedPrice"
    return model
    

MinimumAdvertisedPrice = create_schema_org_model()