"""
MixedEventAttendanceMode - an event that is conducted as a combination of both offline and online modes.

https://schema.org/MixedEventAttendanceMode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MixedEventAttendanceModeInheritedProperties(TypedDict):
    """MixedEventAttendanceMode - an event that is conducted as a combination of both offline and online modes.

    References:
        https://schema.org/MixedEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    


class MixedEventAttendanceModeProperties(TypedDict):
    """MixedEventAttendanceMode - an event that is conducted as a combination of both offline and online modes.

    References:
        https://schema.org/MixedEventAttendanceMode
    Note:
        Model Depth 5
    Attributes:
    """

    

#MixedEventAttendanceModeInheritedPropertiesTd = MixedEventAttendanceModeInheritedProperties()
#MixedEventAttendanceModePropertiesTd = MixedEventAttendanceModeProperties()


class AllProperties(MixedEventAttendanceModeInheritedProperties , MixedEventAttendanceModeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MixedEventAttendanceModeProperties, MixedEventAttendanceModeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MixedEventAttendanceMode"
    return model
    

MixedEventAttendanceMode = create_schema_org_model()