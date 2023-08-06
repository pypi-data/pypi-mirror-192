"""
Scheduling future actions, events, or tasks.Related actions:* [[ReserveAction]]: Unlike ReserveAction, ScheduleAction allocates future actions (e.g. an event, a task, etc) towards a time slot / spatial allocation.

https://schema.org/ScheduleAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ScheduleActionInheritedProperties(TypedDict):
    """Scheduling future actions, events, or tasks.Related actions:* [[ReserveAction]]: Unlike ReserveAction, ScheduleAction allocates future actions (e.g. an event, a task, etc) towards a time slot / spatial allocation.

    References:
        https://schema.org/ScheduleAction
    Note:
        Model Depth 5
    Attributes:
        scheduledTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time the object is scheduled to.
    """

    scheduledTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    


class ScheduleActionProperties(TypedDict):
    """Scheduling future actions, events, or tasks.Related actions:* [[ReserveAction]]: Unlike ReserveAction, ScheduleAction allocates future actions (e.g. an event, a task, etc) towards a time slot / spatial allocation.

    References:
        https://schema.org/ScheduleAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#ScheduleActionInheritedPropertiesTd = ScheduleActionInheritedProperties()
#ScheduleActionPropertiesTd = ScheduleActionProperties()


class AllProperties(ScheduleActionInheritedProperties , ScheduleActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ScheduleActionProperties, ScheduleActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ScheduleAction"
    return model
    

ScheduleAction = create_schema_org_model()