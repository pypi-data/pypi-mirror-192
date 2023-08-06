"""
An agent tracks an object for updates.Related actions:* [[FollowAction]]: Unlike FollowAction, TrackAction refers to the interest on the location of innanimates objects.* [[SubscribeAction]]: Unlike SubscribeAction, TrackAction refers to  the interest on the location of innanimate objects.

https://schema.org/TrackAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TrackActionInheritedProperties(TypedDict):
    """An agent tracks an object for updates.Related actions:* [[FollowAction]]: Unlike FollowAction, TrackAction refers to the interest on the location of innanimates objects.* [[SubscribeAction]]: Unlike SubscribeAction, TrackAction refers to  the interest on the location of innanimate objects.

    References:
        https://schema.org/TrackAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class TrackActionProperties(TypedDict):
    """An agent tracks an object for updates.Related actions:* [[FollowAction]]: Unlike FollowAction, TrackAction refers to the interest on the location of innanimates objects.* [[SubscribeAction]]: Unlike SubscribeAction, TrackAction refers to  the interest on the location of innanimate objects.

    References:
        https://schema.org/TrackAction
    Note:
        Model Depth 4
    Attributes:
        deliveryMethod: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A sub property of instrument. The method of delivery.
    """

    deliveryMethod: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#TrackActionInheritedPropertiesTd = TrackActionInheritedProperties()
#TrackActionPropertiesTd = TrackActionProperties()


class AllProperties(TrackActionInheritedProperties , TrackActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TrackActionProperties, TrackActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TrackAction"
    return model
    

TrackAction = create_schema_org_model()