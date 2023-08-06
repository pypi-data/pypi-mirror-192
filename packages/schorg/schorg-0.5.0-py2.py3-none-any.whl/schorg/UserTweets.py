"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserTweets
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserTweetsInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserTweets
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserTweetsProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserTweets
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserTweetsInheritedPropertiesTd = UserTweetsInheritedProperties()
#UserTweetsPropertiesTd = UserTweetsProperties()


class AllProperties(UserTweetsInheritedProperties , UserTweetsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserTweetsProperties, UserTweetsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserTweets"
    return model
    

UserTweets = create_schema_org_model()