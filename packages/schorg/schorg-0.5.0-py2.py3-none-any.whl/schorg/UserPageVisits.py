"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserPageVisits
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserPageVisitsInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPageVisits
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserPageVisitsProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPageVisits
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserPageVisitsInheritedPropertiesTd = UserPageVisitsInheritedProperties()
#UserPageVisitsPropertiesTd = UserPageVisitsProperties()


class AllProperties(UserPageVisitsInheritedProperties , UserPageVisitsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserPageVisitsProperties, UserPageVisitsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserPageVisits"
    return model
    

UserPageVisits = create_schema_org_model()