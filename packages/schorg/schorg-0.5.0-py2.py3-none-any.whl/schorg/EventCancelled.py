"""
The event has been cancelled. If the event has multiple startDate values, all are assumed to be cancelled. Either startDate or previousStartDate may be used to specify the event's cancelled date(s).

https://schema.org/EventCancelled
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EventCancelledInheritedProperties(TypedDict):
    """The event has been cancelled. If the event has multiple startDate values, all are assumed to be cancelled. Either startDate or previousStartDate may be used to specify the event's cancelled date(s).

    References:
        https://schema.org/EventCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    


class EventCancelledProperties(TypedDict):
    """The event has been cancelled. If the event has multiple startDate values, all are assumed to be cancelled. Either startDate or previousStartDate may be used to specify the event's cancelled date(s).

    References:
        https://schema.org/EventCancelled
    Note:
        Model Depth 6
    Attributes:
    """

    

#EventCancelledInheritedPropertiesTd = EventCancelledInheritedProperties()
#EventCancelledPropertiesTd = EventCancelledProperties()


class AllProperties(EventCancelledInheritedProperties , EventCancelledProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EventCancelledProperties, EventCancelledInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EventCancelled"
    return model
    

EventCancelled = create_schema_org_model()