"""
A blog post.

https://schema.org/BlogPosting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BlogPostingInheritedProperties(TypedDict):
    """A blog post.

    References:
        https://schema.org/BlogPosting
    Note:
        Model Depth 5
    Attributes:
        sharedContent: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A CreativeWork such as an image, video, or audio clip shared as part of this posting.
    """

    sharedContent: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class BlogPostingProperties(TypedDict):
    """A blog post.

    References:
        https://schema.org/BlogPosting
    Note:
        Model Depth 5
    Attributes:
    """

    

#BlogPostingInheritedPropertiesTd = BlogPostingInheritedProperties()
#BlogPostingPropertiesTd = BlogPostingProperties()


class AllProperties(BlogPostingInheritedProperties , BlogPostingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BlogPostingProperties, BlogPostingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BlogPosting"
    return model
    

BlogPosting = create_schema_org_model()