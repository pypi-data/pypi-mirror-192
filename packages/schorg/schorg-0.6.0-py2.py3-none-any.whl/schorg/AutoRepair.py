"""
Car repair business.

https://schema.org/AutoRepair
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoRepairInheritedProperties(TypedDict):
    """Car repair business.

    References:
        https://schema.org/AutoRepair
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoRepairProperties(TypedDict):
    """Car repair business.

    References:
        https://schema.org/AutoRepair
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoRepairInheritedPropertiesTd = AutoRepairInheritedProperties()
#AutoRepairPropertiesTd = AutoRepairProperties()


class AllProperties(AutoRepairInheritedProperties , AutoRepairProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoRepairProperties, AutoRepairInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoRepair"
    return model
    

AutoRepair = create_schema_org_model()