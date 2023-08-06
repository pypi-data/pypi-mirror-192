"""
A subscription which allows a user to access media including audio, video, books, etc.

https://schema.org/MediaSubscription
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MediaSubscriptionInheritedProperties(TypedDict):
    """A subscription which allows a user to access media including audio, video, books, etc.

    References:
        https://schema.org/MediaSubscription
    Note:
        Model Depth 3
    Attributes:
    """

    


class MediaSubscriptionProperties(TypedDict):
    """A subscription which allows a user to access media including audio, video, books, etc.

    References:
        https://schema.org/MediaSubscription
    Note:
        Model Depth 3
    Attributes:
        expectsAcceptanceOf: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An Offer which must be accepted before the user can perform the Action. For example, the user may need to buy a movie before being able to watch it.
        authenticator: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The Organization responsible for authenticating the user's subscription. For example, many media apps require a cable/satellite provider to authenticate your subscription before playing media.
    """

    expectsAcceptanceOf: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    authenticator: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#MediaSubscriptionInheritedPropertiesTd = MediaSubscriptionInheritedProperties()
#MediaSubscriptionPropertiesTd = MediaSubscriptionProperties()


class AllProperties(MediaSubscriptionInheritedProperties , MediaSubscriptionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MediaSubscriptionProperties, MediaSubscriptionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MediaSubscription"
    return model
    

MediaSubscription = create_schema_org_model()