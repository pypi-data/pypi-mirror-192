"""
Enumerates different price types, for example list price, invoice price, and sale price.

https://schema.org/PriceTypeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PriceTypeEnumerationInheritedProperties(TypedDict):
    """Enumerates different price types, for example list price, invoice price, and sale price.

    References:
        https://schema.org/PriceTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class PriceTypeEnumerationProperties(TypedDict):
    """Enumerates different price types, for example list price, invoice price, and sale price.

    References:
        https://schema.org/PriceTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#PriceTypeEnumerationInheritedPropertiesTd = PriceTypeEnumerationInheritedProperties()
#PriceTypeEnumerationPropertiesTd = PriceTypeEnumerationProperties()


class AllProperties(PriceTypeEnumerationInheritedProperties , PriceTypeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PriceTypeEnumerationProperties, PriceTypeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PriceTypeEnumeration"
    return model
    

PriceTypeEnumeration = create_schema_org_model()