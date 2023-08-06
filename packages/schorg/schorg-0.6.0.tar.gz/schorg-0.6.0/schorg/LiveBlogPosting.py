"""
A [[LiveBlogPosting]] is a [[BlogPosting]] intended to provide a rolling textual coverage of an ongoing event through continuous updates.

https://schema.org/LiveBlogPosting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LiveBlogPostingInheritedProperties(TypedDict):
    """A [[LiveBlogPosting]] is a [[BlogPosting]] intended to provide a rolling textual coverage of an ongoing event through continuous updates.

    References:
        https://schema.org/LiveBlogPosting
    Note:
        Model Depth 6
    Attributes:
    """

    


class LiveBlogPostingProperties(TypedDict):
    """A [[LiveBlogPosting]] is a [[BlogPosting]] intended to provide a rolling textual coverage of an ongoing event through continuous updates.

    References:
        https://schema.org/LiveBlogPosting
    Note:
        Model Depth 6
    Attributes:
        liveBlogUpdate: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An update to the LiveBlog.
        coverageStartTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time when the live blog will begin covering the Event. Note that coverage may begin before the Event's start time. The LiveBlogPosting may also be created before coverage begins.
        coverageEndTime: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The time when the live blog will stop covering the Event. Note that coverage may continue after the Event concludes.
    """

    liveBlogUpdate: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    coverageStartTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    coverageEndTime: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    

#LiveBlogPostingInheritedPropertiesTd = LiveBlogPostingInheritedProperties()
#LiveBlogPostingPropertiesTd = LiveBlogPostingProperties()


class AllProperties(LiveBlogPostingInheritedProperties , LiveBlogPostingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LiveBlogPostingProperties, LiveBlogPostingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LiveBlogPosting"
    return model
    

LiveBlogPosting = create_schema_org_model()