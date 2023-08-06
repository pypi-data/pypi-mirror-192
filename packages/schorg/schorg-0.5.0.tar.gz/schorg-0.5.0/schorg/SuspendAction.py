"""
The act of momentarily pausing a device or application (e.g. pause music playback or pause a timer).

https://schema.org/SuspendAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SuspendActionInheritedProperties(TypedDict):
    """The act of momentarily pausing a device or application (e.g. pause music playback or pause a timer).

    References:
        https://schema.org/SuspendAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class SuspendActionProperties(TypedDict):
    """The act of momentarily pausing a device or application (e.g. pause music playback or pause a timer).

    References:
        https://schema.org/SuspendAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#SuspendActionInheritedPropertiesTd = SuspendActionInheritedProperties()
#SuspendActionPropertiesTd = SuspendActionProperties()


class AllProperties(SuspendActionInheritedProperties , SuspendActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SuspendActionProperties, SuspendActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SuspendAction"
    return model
    

SuspendAction = create_schema_org_model()