"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserDownloads
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserDownloadsInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserDownloads
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserDownloadsProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserDownloads
    Note:
        Model Depth 4
    Attributes:
    """

    

#UserDownloadsInheritedPropertiesTd = UserDownloadsInheritedProperties()
#UserDownloadsPropertiesTd = UserDownloadsProperties()


class AllProperties(UserDownloadsInheritedProperties , UserDownloadsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserDownloadsProperties, UserDownloadsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserDownloads"
    return model
    

UserDownloads = create_schema_org_model()