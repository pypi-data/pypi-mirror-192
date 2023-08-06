"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserCheckins
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserCheckinsInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserCheckins
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserCheckinsProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserCheckins
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserCheckinsInheritedPropertiesTd = UserCheckinsInheritedProperties()
#UserCheckinsPropertiesTd = UserCheckinsProperties()


class AllProperties(UserCheckinsInheritedProperties , UserCheckinsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserCheckinsProperties, UserCheckinsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserCheckins"
    return model
    

UserCheckins = create_schema_org_model()