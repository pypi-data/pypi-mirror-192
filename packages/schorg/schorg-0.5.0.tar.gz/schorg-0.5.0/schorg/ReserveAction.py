"""
Reserving a concrete object.Related actions:* [[ScheduleAction]]: Unlike ScheduleAction, ReserveAction reserves concrete objects (e.g. a table, a hotel) towards a time slot / spatial allocation.

https://schema.org/ReserveAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReserveActionInheritedProperties(TypedDict):
    """Reserving a concrete object.Related actions:* [[ScheduleAction]]: Unlike ScheduleAction, ReserveAction reserves concrete objects (e.g. a table, a hotel) towards a time slot / spatial allocation.

    References:
        https://schema.org/ReserveAction
    Note:
        Model Depth 5
    Attributes:
        scheduledTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time the object is scheduled to.
    """

    scheduledTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    


class ReserveActionProperties(TypedDict):
    """Reserving a concrete object.Related actions:* [[ScheduleAction]]: Unlike ScheduleAction, ReserveAction reserves concrete objects (e.g. a table, a hotel) towards a time slot / spatial allocation.

    References:
        https://schema.org/ReserveAction
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReserveActionInheritedPropertiesTd = ReserveActionInheritedProperties()
#ReserveActionPropertiesTd = ReserveActionProperties()


class AllProperties(ReserveActionInheritedProperties , ReserveActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReserveActionProperties, ReserveActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReserveAction"
    return model
    

ReserveAction = create_schema_org_model()