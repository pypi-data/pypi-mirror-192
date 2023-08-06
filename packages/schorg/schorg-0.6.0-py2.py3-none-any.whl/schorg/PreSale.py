"""
Indicates that the item is available for ordering and delivery before general availability.

https://schema.org/PreSale
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PreSaleInheritedProperties(TypedDict):
    """Indicates that the item is available for ordering and delivery before general availability.

    References:
        https://schema.org/PreSale
    Note:
        Model Depth 5
    Attributes:
    """

    


class PreSaleProperties(TypedDict):
    """Indicates that the item is available for ordering and delivery before general availability.

    References:
        https://schema.org/PreSale
    Note:
        Model Depth 5
    Attributes:
    """

    

#PreSaleInheritedPropertiesTd = PreSaleInheritedProperties()
#PreSalePropertiesTd = PreSaleProperties()


class AllProperties(PreSaleInheritedProperties , PreSaleProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PreSaleProperties, PreSaleInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PreSale"
    return model
    

PreSale = create_schema_org_model()