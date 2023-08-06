"""
Indicates that the event was changed to allow online participation. See [[eventAttendanceMode]] for specifics of whether it is now fully or partially online.

https://schema.org/EventMovedOnline
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EventMovedOnlineInheritedProperties(TypedDict):
    """Indicates that the event was changed to allow online participation. See [[eventAttendanceMode]] for specifics of whether it is now fully or partially online.

    References:
        https://schema.org/EventMovedOnline
    Note:
        Model Depth 6
    Attributes:
    """

    


class EventMovedOnlineProperties(TypedDict):
    """Indicates that the event was changed to allow online participation. See [[eventAttendanceMode]] for specifics of whether it is now fully or partially online.

    References:
        https://schema.org/EventMovedOnline
    Note:
        Model Depth 6
    Attributes:
    """

    

#EventMovedOnlineInheritedPropertiesTd = EventMovedOnlineInheritedProperties()
#EventMovedOnlinePropertiesTd = EventMovedOnlineProperties()


class AllProperties(EventMovedOnlineInheritedProperties , EventMovedOnlineProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EventMovedOnlineProperties, EventMovedOnlineInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EventMovedOnline"
    return model
    

EventMovedOnline = create_schema_org_model()