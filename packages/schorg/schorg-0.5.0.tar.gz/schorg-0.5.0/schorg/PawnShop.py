"""
A shop that will buy, or lend money against the security of, personal possessions.

https://schema.org/PawnShop
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PawnShopInheritedProperties(TypedDict):
    """A shop that will buy, or lend money against the security of, personal possessions.

    References:
        https://schema.org/PawnShop
    Note:
        Model Depth 5
    Attributes:
    """

    


class PawnShopProperties(TypedDict):
    """A shop that will buy, or lend money against the security of, personal possessions.

    References:
        https://schema.org/PawnShop
    Note:
        Model Depth 5
    Attributes:
    """

    

#PawnShopInheritedPropertiesTd = PawnShopInheritedProperties()
#PawnShopPropertiesTd = PawnShopProperties()


class AllProperties(PawnShopInheritedProperties , PawnShopProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PawnShopProperties, PawnShopInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PawnShop"
    return model
    

PawnShop = create_schema_org_model()