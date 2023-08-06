"""
A [[comment]] that corrects [[CreativeWork]].

https://schema.org/CorrectionComment
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CorrectionCommentInheritedProperties(TypedDict):
    """A [[comment]] that corrects [[CreativeWork]].

    References:
        https://schema.org/CorrectionComment
    Note:
        Model Depth 4
    Attributes:
        parentItem: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The parent of a question, answer or item in general.
        downvoteCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of downvotes this question, answer or comment has received from the community.
        upvoteCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of upvotes this question, answer or comment has received from the community.
    """

    parentItem: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    downvoteCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    upvoteCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class CorrectionCommentProperties(TypedDict):
    """A [[comment]] that corrects [[CreativeWork]].

    References:
        https://schema.org/CorrectionComment
    Note:
        Model Depth 4
    Attributes:
    """

    

#CorrectionCommentInheritedPropertiesTd = CorrectionCommentInheritedProperties()
#CorrectionCommentPropertiesTd = CorrectionCommentProperties()


class AllProperties(CorrectionCommentInheritedProperties , CorrectionCommentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CorrectionCommentProperties, CorrectionCommentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CorrectionComment"
    return model
    

CorrectionComment = create_schema_org_model()