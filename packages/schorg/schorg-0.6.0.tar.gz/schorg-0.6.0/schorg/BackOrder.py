"""
Indicates that the item is available on back order.

https://schema.org/BackOrder
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BackOrderInheritedProperties(TypedDict):
    """Indicates that the item is available on back order.

    References:
        https://schema.org/BackOrder
    Note:
        Model Depth 5
    Attributes:
    """

    


class BackOrderProperties(TypedDict):
    """Indicates that the item is available on back order.

    References:
        https://schema.org/BackOrder
    Note:
        Model Depth 5
    Attributes:
    """

    

#BackOrderInheritedPropertiesTd = BackOrderInheritedProperties()
#BackOrderPropertiesTd = BackOrderProperties()


class AllProperties(BackOrderInheritedProperties , BackOrderProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BackOrderProperties, BackOrderInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BackOrder"
    return model
    

BackOrder = create_schema_org_model()