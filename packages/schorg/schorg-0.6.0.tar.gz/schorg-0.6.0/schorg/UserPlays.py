"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserPlays
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserPlaysInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPlays
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserPlaysProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPlays
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserPlaysInheritedPropertiesTd = UserPlaysInheritedProperties()
#UserPlaysPropertiesTd = UserPlaysProperties()


class AllProperties(UserPlaysInheritedProperties , UserPlaysProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserPlaysProperties, UserPlaysInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserPlays"
    return model
    

UserPlays = create_schema_org_model()