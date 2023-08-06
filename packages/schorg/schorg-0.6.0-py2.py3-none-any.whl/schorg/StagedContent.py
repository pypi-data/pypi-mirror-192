"""
Content coded 'staged content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'staged content': A video that has been created using actors or similarly contrived.For an [[ImageObject]] to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[ImageObject]] with embedded text to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[AudioObject]] to be 'staged content': Audio that has been created using actors or similarly contrived.

https://schema.org/StagedContent
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class StagedContentInheritedProperties(TypedDict):
    """Content coded 'staged content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'staged content': A video that has been created using actors or similarly contrived.For an [[ImageObject]] to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[ImageObject]] with embedded text to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[AudioObject]] to be 'staged content': Audio that has been created using actors or similarly contrived.

    References:
        https://schema.org/StagedContent
    Note:
        Model Depth 5
    Attributes:
    """

    


class StagedContentProperties(TypedDict):
    """Content coded 'staged content' in a [[MediaReview]], considered in the context of how it was published or shared.For a [[VideoObject]] to be 'staged content': A video that has been created using actors or similarly contrived.For an [[ImageObject]] to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[ImageObject]] with embedded text to be 'staged content': An image that was created using actors or similarly contrived, such as a screenshot of a fake tweet.For an [[AudioObject]] to be 'staged content': Audio that has been created using actors or similarly contrived.

    References:
        https://schema.org/StagedContent
    Note:
        Model Depth 5
    Attributes:
    """

    

#StagedContentInheritedPropertiesTd = StagedContentInheritedProperties()
#StagedContentPropertiesTd = StagedContentProperties()


class AllProperties(StagedContentInheritedProperties , StagedContentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[StagedContentProperties, StagedContentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "StagedContent"
    return model
    

StagedContent = create_schema_org_model()