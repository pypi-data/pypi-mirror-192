"""
A tire shop.

https://schema.org/TireShop
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TireShopInheritedProperties(TypedDict):
    """A tire shop.

    References:
        https://schema.org/TireShop
    Note:
        Model Depth 5
    Attributes:
    """

    


class TireShopProperties(TypedDict):
    """A tire shop.

    References:
        https://schema.org/TireShop
    Note:
        Model Depth 5
    Attributes:
    """

    

#TireShopInheritedPropertiesTd = TireShopInheritedProperties()
#TireShopPropertiesTd = TireShopProperties()


class AllProperties(TireShopInheritedProperties , TireShopProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TireShopProperties, TireShopInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TireShop"
    return model
    

TireShop = create_schema_org_model()