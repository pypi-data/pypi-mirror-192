"""
Specifies that the customer must pay a restocking fee when returning a product.

https://schema.org/RestockingFees
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RestockingFeesInheritedProperties(TypedDict):
    """Specifies that the customer must pay a restocking fee when returning a product.

    References:
        https://schema.org/RestockingFees
    Note:
        Model Depth 5
    Attributes:
    """

    


class RestockingFeesProperties(TypedDict):
    """Specifies that the customer must pay a restocking fee when returning a product.

    References:
        https://schema.org/RestockingFees
    Note:
        Model Depth 5
    Attributes:
    """

    

#RestockingFeesInheritedPropertiesTd = RestockingFeesInheritedProperties()
#RestockingFeesPropertiesTd = RestockingFeesProperties()


class AllProperties(RestockingFeesInheritedProperties , RestockingFeesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RestockingFeesProperties, RestockingFeesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RestockingFees"
    return model
    

RestockingFees = create_schema_org_model()