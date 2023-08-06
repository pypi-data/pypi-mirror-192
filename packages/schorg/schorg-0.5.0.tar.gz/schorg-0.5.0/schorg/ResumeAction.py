"""
The act of resuming a device or application which was formerly paused (e.g. resume music playback or resume a timer).

https://schema.org/ResumeAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ResumeActionInheritedProperties(TypedDict):
    """The act of resuming a device or application which was formerly paused (e.g. resume music playback or resume a timer).

    References:
        https://schema.org/ResumeAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class ResumeActionProperties(TypedDict):
    """The act of resuming a device or application which was formerly paused (e.g. resume music playback or resume a timer).

    References:
        https://schema.org/ResumeAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#ResumeActionInheritedPropertiesTd = ResumeActionInheritedProperties()
#ResumeActionPropertiesTd = ResumeActionProperties()


class AllProperties(ResumeActionInheritedProperties , ResumeActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ResumeActionProperties, ResumeActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ResumeAction"
    return model
    

ResumeAction = create_schema_org_model()