"""
PaidLeave: this is a benefit for paid leave.

https://schema.org/PaidLeave
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PaidLeaveInheritedProperties(TypedDict):
    """PaidLeave: this is a benefit for paid leave.

    References:
        https://schema.org/PaidLeave
    Note:
        Model Depth 5
    Attributes:
    """

    


class PaidLeaveProperties(TypedDict):
    """PaidLeave: this is a benefit for paid leave.

    References:
        https://schema.org/PaidLeave
    Note:
        Model Depth 5
    Attributes:
    """

    

#PaidLeaveInheritedPropertiesTd = PaidLeaveInheritedProperties()
#PaidLeavePropertiesTd = PaidLeaveProperties()


class AllProperties(PaidLeaveInheritedProperties , PaidLeaveProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PaidLeaveProperties, PaidLeaveInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PaidLeave"
    return model
    

PaidLeave = create_schema_org_model()