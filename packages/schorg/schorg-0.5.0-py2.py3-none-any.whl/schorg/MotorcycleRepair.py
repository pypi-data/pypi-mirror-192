"""
A motorcycle repair shop.

https://schema.org/MotorcycleRepair
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MotorcycleRepairInheritedProperties(TypedDict):
    """A motorcycle repair shop.

    References:
        https://schema.org/MotorcycleRepair
    Note:
        Model Depth 5
    Attributes:
    """

    


class MotorcycleRepairProperties(TypedDict):
    """A motorcycle repair shop.

    References:
        https://schema.org/MotorcycleRepair
    Note:
        Model Depth 5
    Attributes:
    """

    

#MotorcycleRepairInheritedPropertiesTd = MotorcycleRepairInheritedProperties()
#MotorcycleRepairPropertiesTd = MotorcycleRepairProperties()


class AllProperties(MotorcycleRepairInheritedProperties , MotorcycleRepairProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MotorcycleRepairProperties, MotorcycleRepairInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MotorcycleRepair"
    return model
    

MotorcycleRepair = create_schema_org_model()