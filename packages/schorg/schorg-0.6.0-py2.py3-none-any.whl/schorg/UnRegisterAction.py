"""
The act of un-registering from a service.Related actions:* [[RegisterAction]]: antonym of UnRegisterAction.* [[LeaveAction]]: Unlike LeaveAction, UnRegisterAction implies that you are unregistering from a service you were previously registered, rather than leaving a team/group of people.

https://schema.org/UnRegisterAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UnRegisterActionInheritedProperties(TypedDict):
    """The act of un-registering from a service.Related actions:* [[RegisterAction]]: antonym of UnRegisterAction.* [[LeaveAction]]: Unlike LeaveAction, UnRegisterAction implies that you are unregistering from a service you were previously registered, rather than leaving a team/group of people.

    References:
        https://schema.org/UnRegisterAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class UnRegisterActionProperties(TypedDict):
    """The act of un-registering from a service.Related actions:* [[RegisterAction]]: antonym of UnRegisterAction.* [[LeaveAction]]: Unlike LeaveAction, UnRegisterAction implies that you are unregistering from a service you were previously registered, rather than leaving a team/group of people.

    References:
        https://schema.org/UnRegisterAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#UnRegisterActionInheritedPropertiesTd = UnRegisterActionInheritedProperties()
#UnRegisterActionPropertiesTd = UnRegisterActionProperties()


class AllProperties(UnRegisterActionInheritedProperties , UnRegisterActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UnRegisterActionProperties, UnRegisterActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UnRegisterAction"
    return model
    

UnRegisterAction = create_schema_org_model()