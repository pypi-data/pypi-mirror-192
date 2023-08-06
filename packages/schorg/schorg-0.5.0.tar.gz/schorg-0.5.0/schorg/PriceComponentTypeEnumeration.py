"""
Enumerates different price components that together make up the total price for an offered product.

https://schema.org/PriceComponentTypeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PriceComponentTypeEnumerationInheritedProperties(TypedDict):
    """Enumerates different price components that together make up the total price for an offered product.

    References:
        https://schema.org/PriceComponentTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PriceComponentTypeEnumerationProperties(TypedDict):
    """Enumerates different price components that together make up the total price for an offered product.

    References:
        https://schema.org/PriceComponentTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#PriceComponentTypeEnumerationInheritedPropertiesTd = PriceComponentTypeEnumerationInheritedProperties()
#PriceComponentTypeEnumerationPropertiesTd = PriceComponentTypeEnumerationProperties()


class AllProperties(PriceComponentTypeEnumerationInheritedProperties , PriceComponentTypeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PriceComponentTypeEnumerationProperties, PriceComponentTypeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PriceComponentTypeEnumeration"
    return model
    

PriceComponentTypeEnumeration = create_schema_org_model()