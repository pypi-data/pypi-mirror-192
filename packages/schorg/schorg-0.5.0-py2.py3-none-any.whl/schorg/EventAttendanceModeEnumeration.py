"""
An EventAttendanceModeEnumeration value is one of potentially several modes of organising an event, relating to whether it is online or offline.

https://schema.org/EventAttendanceModeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EventAttendanceModeEnumerationInheritedProperties(TypedDict):
    """An EventAttendanceModeEnumeration value is one of potentially several modes of organising an event, relating to whether it is online or offline.

    References:
        https://schema.org/EventAttendanceModeEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class EventAttendanceModeEnumerationProperties(TypedDict):
    """An EventAttendanceModeEnumeration value is one of potentially several modes of organising an event, relating to whether it is online or offline.

    References:
        https://schema.org/EventAttendanceModeEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#EventAttendanceModeEnumerationInheritedPropertiesTd = EventAttendanceModeEnumerationInheritedProperties()
#EventAttendanceModeEnumerationPropertiesTd = EventAttendanceModeEnumerationProperties()


class AllProperties(EventAttendanceModeEnumerationInheritedProperties , EventAttendanceModeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EventAttendanceModeEnumerationProperties, EventAttendanceModeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EventAttendanceModeEnumeration"
    return model
    

EventAttendanceModeEnumeration = create_schema_org_model()