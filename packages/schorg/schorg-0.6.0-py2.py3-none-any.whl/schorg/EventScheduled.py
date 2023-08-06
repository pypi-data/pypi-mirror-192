"""
The event is taking place or has taken place on the startDate as scheduled. Use of this value is optional, as it is assumed by default.

https://schema.org/EventScheduled
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EventScheduledInheritedProperties(TypedDict):
    """The event is taking place or has taken place on the startDate as scheduled. Use of this value is optional, as it is assumed by default.

    References:
        https://schema.org/EventScheduled
    Note:
        Model Depth 6
    Attributes:
    """

    


class EventScheduledProperties(TypedDict):
    """The event is taking place or has taken place on the startDate as scheduled. Use of this value is optional, as it is assumed by default.

    References:
        https://schema.org/EventScheduled
    Note:
        Model Depth 6
    Attributes:
    """

    

#EventScheduledInheritedPropertiesTd = EventScheduledInheritedProperties()
#EventScheduledPropertiesTd = EventScheduledProperties()


class AllProperties(EventScheduledInheritedProperties , EventScheduledProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EventScheduledProperties, EventScheduledInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EventScheduled"
    return model
    

EventScheduled = create_schema_org_model()