"""
OfflineEventAttendanceMode - an event that is primarily conducted offline. 

https://schema.org/OfflineEventAttendanceMode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OfflineEventAttendanceModeInheritedProperties(TypedDict):
    """OfflineEventAttendanceMode - an event that is primarily conducted offline. 

    References:
        https://schema.org/OfflineEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    


class OfflineEventAttendanceModeProperties(TypedDict):
    """OfflineEventAttendanceMode - an event that is primarily conducted offline. 

    References:
        https://schema.org/OfflineEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    

#OfflineEventAttendanceModeInheritedPropertiesTd = OfflineEventAttendanceModeInheritedProperties()
#OfflineEventAttendanceModePropertiesTd = OfflineEventAttendanceModeProperties()


class AllProperties(OfflineEventAttendanceModeInheritedProperties , OfflineEventAttendanceModeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OfflineEventAttendanceModeProperties, OfflineEventAttendanceModeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OfflineEventAttendanceMode"
    return model
    

OfflineEventAttendanceMode = create_schema_org_model()