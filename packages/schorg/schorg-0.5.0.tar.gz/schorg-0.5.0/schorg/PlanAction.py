"""
The act of planning the execution of an event/task/action/reservation/plan to a future date.

https://schema.org/PlanAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PlanActionInheritedProperties(TypedDict):
    """The act of planning the execution of an event/task/action/reservation/plan to a future date.

    References:
        https://schema.org/PlanAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class PlanActionProperties(TypedDict):
    """The act of planning the execution of an event/task/action/reservation/plan to a future date.

    References:
        https://schema.org/PlanAction
    Note:
        Model Depth 4
    Attributes:
        scheduledTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time the object is scheduled to.
    """

    scheduledTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    

#PlanActionInheritedPropertiesTd = PlanActionInheritedProperties()
#PlanActionPropertiesTd = PlanActionProperties()


class AllProperties(PlanActionInheritedProperties , PlanActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PlanActionProperties, PlanActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PlanAction"
    return model
    

PlanAction = create_schema_org_model()