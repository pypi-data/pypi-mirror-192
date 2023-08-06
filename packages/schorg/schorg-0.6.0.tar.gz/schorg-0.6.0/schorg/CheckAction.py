"""
An agent inspects, determines, investigates, inquires, or examines an object's accuracy, quality, condition, or state.

https://schema.org/CheckAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CheckActionInheritedProperties(TypedDict):
    """An agent inspects, determines, investigates, inquires, or examines an object's accuracy, quality, condition, or state.

    References:
        https://schema.org/CheckAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class CheckActionProperties(TypedDict):
    """An agent inspects, determines, investigates, inquires, or examines an object's accuracy, quality, condition, or state.

    References:
        https://schema.org/CheckAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#CheckActionInheritedPropertiesTd = CheckActionInheritedProperties()
#CheckActionPropertiesTd = CheckActionProperties()


class AllProperties(CheckActionInheritedProperties , CheckActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CheckActionProperties, CheckActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CheckAction"
    return model
    

CheckAction = create_schema_org_model()