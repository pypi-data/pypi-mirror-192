"""
UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

https://schema.org/UserComments
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class UserCommentsInheritedProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserComments
    Note:
        Model Depth 4
    Attributes:
    """

    


class UserCommentsProperties(TypedDict):
    """UserInteraction and its subtypes is an old way of talking about users interacting with pages. It is generally better to use [[Action]]-based vocabulary, alongside types such as [[Comment]].

    References:
        https://schema.org/UserComments
    Note:
        Model Depth 4
    Attributes:
        commentText: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The text of the UserComment.
        replyToUrl: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): The URL at which a reply may be posted to the specified UserComment.
        creator: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The creator/author of this CreativeWork. This is the same as the Author property for CreativeWork.
        commentTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]): The time at which the UserComment was made.
        discusses: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Specifies the CreativeWork associated with the UserComment.
    """

    commentText: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    replyToUrl: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    creator: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    commentTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str, date]], datetime, SchemaOrgObj, str, date]]
    discusses: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#UserCommentsInheritedPropertiesTd = UserCommentsInheritedProperties()
#UserCommentsPropertiesTd = UserCommentsProperties()


class AllProperties(UserCommentsInheritedProperties , UserCommentsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[UserCommentsProperties, UserCommentsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "UserComments"
    return model
    

UserComments = create_schema_org_model()