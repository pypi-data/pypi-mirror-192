"""
A posting to a discussion forum.

https://schema.org/DiscussionForumPosting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiscussionForumPostingInheritedProperties(TypedDict):
    """A posting to a discussion forum.

    References:
        https://schema.org/DiscussionForumPosting
    Note:
        Model Depth 5
    Attributes:
        sharedContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A CreativeWork such as an image, video, or audio clip shared as part of this posting.
    """

    sharedContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class DiscussionForumPostingProperties(TypedDict):
    """A posting to a discussion forum.

    References:
        https://schema.org/DiscussionForumPosting
    Note:
        Model Depth 5
    Attributes:
    """

    

#DiscussionForumPostingInheritedPropertiesTd = DiscussionForumPostingInheritedProperties()
#DiscussionForumPostingPropertiesTd = DiscussionForumPostingProperties()


class AllProperties(DiscussionForumPostingInheritedProperties , DiscussionForumPostingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiscussionForumPostingProperties, DiscussionForumPostingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DiscussionForumPosting"
    return model
    

DiscussionForumPosting = create_schema_org_model()