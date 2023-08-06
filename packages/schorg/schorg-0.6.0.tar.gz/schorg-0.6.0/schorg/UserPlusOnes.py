"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserPlusOnes
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserPlusOnesInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPlusOnes
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserPlusOnesProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserPlusOnes
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserPlusOnesInheritedPropertiesTd = UserPlusOnesInheritedProperties()
#UserPlusOnesPropertiesTd = UserPlusOnesProperties()


class AllProperties(UserPlusOnesInheritedProperties , UserPlusOnesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserPlusOnesProperties, UserPlusOnesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserPlusOnes"
    return model
    

UserPlusOnes = create_schema_org_model()