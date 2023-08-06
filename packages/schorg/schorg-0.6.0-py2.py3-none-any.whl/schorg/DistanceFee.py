"""
Represents the distance fee (e.g., price per km or mile) part of the total price for an offered product, for example a car rental.

https://schema.org/DistanceFee
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DistanceFeeInheritedProperties(TypedDict):
    """Represents the distance fee (e.g., price per km or mile) part of the total price for an offered product, for example a car rental.

    References:
        https://schema.org/DistanceFee
    Note:
        Model Depth 5
    Attributes:
    """

    


class DistanceFeeProperties(TypedDict):
    """Represents the distance fee (e.g., price per km or mile) part of the total price for an offered product, for example a car rental.

    References:
        https://schema.org/DistanceFee
    Note:
        Model Depth 5
    Attributes:
    """

    

#DistanceFeeInheritedPropertiesTd = DistanceFeeInheritedProperties()
#DistanceFeePropertiesTd = DistanceFeeProperties()


class AllProperties(DistanceFeeInheritedProperties , DistanceFeeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DistanceFeeProperties, DistanceFeeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DistanceFee"
    return model
    

DistanceFee = create_schema_org_model()