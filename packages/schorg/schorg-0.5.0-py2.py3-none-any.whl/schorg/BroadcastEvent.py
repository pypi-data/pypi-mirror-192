"""
An over the air or online broadcast event.

https://schema.org/BroadcastEvent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BroadcastEventInheritedProperties(TypedDict):
    """An over the air or online broadcast event.

    References:
        https://schema.org/BroadcastEvent
    Note:
        Model Depth 4
    Attributes:
        publishedBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An agent associated with the publication event.
        free: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): A flag to signal that the item, event, or place is accessible for free.
        publishedOn: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A broadcast service associated with the publication event.
    """

    publishedBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    free: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    publishedOn: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class BroadcastEventProperties(TypedDict):
    """An over the air or online broadcast event.

    References:
        https://schema.org/BroadcastEvent
    Note:
        Model Depth 4
    Attributes:
        subtitleLanguage: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Languages in which subtitles/captions are available, in [IETF BCP 47 standard format](http://tools.ietf.org/html/bcp47).
        broadcastOfEvent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The event being broadcast such as a sporting event or awards ceremony.
        videoFormat: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The type of screening or video broadcast used (e.g. IMAX, 3D, SD, HD, etc.).
        isLiveBroadcast: (Optional[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]): True if the broadcast is of a live event.
    """

    subtitleLanguage: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    broadcastOfEvent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    videoFormat: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    isLiveBroadcast: NotRequired[Union[List[Union[StrictBool, SchemaOrgObj, str]], StrictBool, SchemaOrgObj, str]]
    

#BroadcastEventInheritedPropertiesTd = BroadcastEventInheritedProperties()
#BroadcastEventPropertiesTd = BroadcastEventProperties()


class AllProperties(BroadcastEventInheritedProperties , BroadcastEventProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BroadcastEventProperties, BroadcastEventInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BroadcastEvent"
    return model
    

BroadcastEvent = create_schema_org_model()