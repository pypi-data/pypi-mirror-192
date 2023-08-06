"""
An agent leaves an event / group with participants/friends at a location.Related actions:* [[JoinAction]]: The antonym of LeaveAction.* [[UnRegisterAction]]: Unlike UnRegisterAction, LeaveAction implies leaving a group/team of people rather than a service.

https://schema.org/LeaveAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LeaveActionInheritedProperties(TypedDict):
    """An agent leaves an event / group with participants/friends at a location.Related actions:* [[JoinAction]]: The antonym of LeaveAction.* [[UnRegisterAction]]: Unlike UnRegisterAction, LeaveAction implies leaving a group/team of people rather than a service.

    References:
        https://schema.org/LeaveAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class LeaveActionProperties(TypedDict):
    """An agent leaves an event / group with participants/friends at a location.Related actions:* [[JoinAction]]: The antonym of LeaveAction.* [[UnRegisterAction]]: Unlike UnRegisterAction, LeaveAction implies leaving a group/team of people rather than a service.

    References:
        https://schema.org/LeaveAction
    Note:
        Model Depth 4
    Attributes:
        event: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Upcoming or past event associated with this place, organization, or action.
    """

    event: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#LeaveActionInheritedPropertiesTd = LeaveActionInheritedProperties()
#LeaveActionPropertiesTd = LeaveActionProperties()


class AllProperties(LeaveActionInheritedProperties , LeaveActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LeaveActionProperties, LeaveActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LeaveAction"
    return model
    

LeaveAction = create_schema_org_model()