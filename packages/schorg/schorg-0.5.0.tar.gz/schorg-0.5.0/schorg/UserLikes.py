"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserLikes
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserLikesInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserLikes
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserLikesProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserLikes
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserLikesInheritedPropertiesTd = UserLikesInheritedProperties()
#UserLikesPropertiesTd = UserLikesProperties()


class AllProperties(UserLikesInheritedProperties , UserLikesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserLikesProperties, UserLikesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserLikes"
    return model
    

UserLikes = create_schema_org_model()