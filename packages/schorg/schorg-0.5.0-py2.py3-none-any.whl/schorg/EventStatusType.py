"""
EventStatusType is an enumeration type whose instances represent several states that an Event may be in.

https://schema.org/EventStatusType
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EventStatusTypeInheritedProperties(TypedDict):
    """EventStatusType is an enumeration type whose instances represent several states that an Event may be in.

    References:
        https://schema.org/EventStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    


class EventStatusTypeProperties(TypedDict):
    """EventStatusType is an enumeration type whose instances represent several states that an Event may be in.

    References:
        https://schema.org/EventStatusType
    Note:
        Model Depth 5
    Attributes:
    """

    

#EventStatusTypeInheritedPropertiesTd = EventStatusTypeInheritedProperties()
#EventStatusTypePropertiesTd = EventStatusTypeProperties()


class AllProperties(EventStatusTypeInheritedProperties , EventStatusTypeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EventStatusTypeProperties, EventStatusTypeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EventStatusType"
    return model
    

EventStatusType = create_schema_org_model()