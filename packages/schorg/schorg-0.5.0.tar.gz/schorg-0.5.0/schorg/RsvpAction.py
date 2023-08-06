"""
The act of notifying an event organizer as to whether you expect to attend the event.

https://schema.org/RsvpAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RsvpActionInheritedProperties(TypedDict):
    """The act of notifying an event organizer as to whether you expect to attend the event.

    References:
        https://schema.org/RsvpAction
    Note:
        Model Depth 6
    Attributes:
        event: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Upcoming or past event associated with this place, organization, or action.
    """

    event: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class RsvpActionProperties(TypedDict):
    """The act of notifying an event organizer as to whether you expect to attend the event.

    References:
        https://schema.org/RsvpAction
    Note:
        Model Depth 6
    Attributes:
        additionalNumberOfGuests: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): If responding yes, the number of guests who will attend in addition to the invitee.
        comment: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Comments, typically from users.
        rsvpResponse: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The response (yes, no, maybe) to the RSVP.
    """

    additionalNumberOfGuests: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    comment: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    rsvpResponse: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#RsvpActionInheritedPropertiesTd = RsvpActionInheritedProperties()
#RsvpActionPropertiesTd = RsvpActionProperties()


class AllProperties(RsvpActionInheritedProperties , RsvpActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RsvpActionProperties, RsvpActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RsvpAction"
    return model
    

RsvpAction = create_schema_org_model()