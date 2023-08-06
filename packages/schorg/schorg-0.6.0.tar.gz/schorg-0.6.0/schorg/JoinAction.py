"""
An agent joins an event/group with participants/friends at a location.Related actions:* [[RegisterAction]]: Unlike RegisterAction, JoinAction refers to joining a group/team of people.* [[SubscribeAction]]: Unlike SubscribeAction, JoinAction does not imply that you'll be receiving updates.* [[FollowAction]]: Unlike FollowAction, JoinAction does not imply that you'll be polling for updates.

https://schema.org/JoinAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class JoinActionInheritedProperties(TypedDict):
    """An agent joins an event/group with participants/friends at a location.Related actions:* [[RegisterAction]]: Unlike RegisterAction, JoinAction refers to joining a group/team of people.* [[SubscribeAction]]: Unlike SubscribeAction, JoinAction does not imply that you'll be receiving updates.* [[FollowAction]]: Unlike FollowAction, JoinAction does not imply that you'll be polling for updates.

    References:
        https://schema.org/JoinAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class JoinActionProperties(TypedDict):
    """An agent joins an event/group with participants/friends at a location.Related actions:* [[RegisterAction]]: Unlike RegisterAction, JoinAction refers to joining a group/team of people.* [[SubscribeAction]]: Unlike SubscribeAction, JoinAction does not imply that you'll be receiving updates.* [[FollowAction]]: Unlike FollowAction, JoinAction does not imply that you'll be polling for updates.

    References:
        https://schema.org/JoinAction
    Note:
        Model Depth 4
    Attributes:
        event: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Upcoming or past event associated with this place, organization, or action.
    """

    event: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#JoinActionInheritedPropertiesTd = JoinActionInheritedProperties()
#JoinActionPropertiesTd = JoinActionProperties()


class AllProperties(JoinActionInheritedProperties , JoinActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[JoinActionProperties, JoinActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "JoinAction"
    return model
    

JoinAction = create_schema_org_model()