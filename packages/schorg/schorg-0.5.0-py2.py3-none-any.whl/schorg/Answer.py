"""
An answer offered to a question; perhaps correct, perhaps opinionated or wrong.

https://schema.org/Answer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AnswerInheritedProperties(TypedDict):
    """An answer offered to a question; perhaps correct, perhaps opinionated or wrong.

    References:
        https://schema.org/Answer
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
    


class AnswerProperties(TypedDict):
    """An answer offered to a question; perhaps correct, perhaps opinionated or wrong.

    References:
        https://schema.org/Answer
    Note:
        Model Depth 4
    Attributes:
        answerExplanation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): A step-by-step or full explanation about Answer. Can outline how this Answer was achieved or contain more broad clarification or statement about it. 
    """

    answerExplanation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#AnswerInheritedPropertiesTd = AnswerInheritedProperties()
#AnswerPropertiesTd = AnswerProperties()


class AllProperties(AnswerInheritedProperties , AnswerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AnswerProperties, AnswerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Answer"
    return model
    

Answer = create_schema_org_model()