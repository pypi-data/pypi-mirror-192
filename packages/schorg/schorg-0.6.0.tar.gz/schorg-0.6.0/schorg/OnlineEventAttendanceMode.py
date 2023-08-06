"""
OnlineEventAttendanceMode - an event that is primarily conducted online. 

https://schema.org/OnlineEventAttendanceMode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OnlineEventAttendanceModeInheritedProperties(TypedDict):
    """OnlineEventAttendanceMode - an event that is primarily conducted online. 

    References:
        https://schema.org/OnlineEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    


class OnlineEventAttendanceModeProperties(TypedDict):
    """OnlineEventAttendanceMode - an event that is primarily conducted online. 

    References:
        https://schema.org/OnlineEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    

#OnlineEventAttendanceModeInheritedPropertiesTd = OnlineEventAttendanceModeInheritedProperties()
#OnlineEventAttendanceModePropertiesTd = OnlineEventAttendanceModeProperties()


class AllProperties(OnlineEventAttendanceModeInheritedProperties , OnlineEventAttendanceModeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OnlineEventAttendanceModeProperties, OnlineEventAttendanceModeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OnlineEventAttendanceMode"
    return model
    

OnlineEventAttendanceMode = create_schema_org_model()