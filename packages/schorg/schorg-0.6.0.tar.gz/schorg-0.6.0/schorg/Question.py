"""
A specific question - e.g. from a user seeking answers online, or collected in a Frequently Asked Questions (FAQ) document.

https://schema.org/Question
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class QuestionInheritedProperties(TypedDict):
    """A specific question - e.g. from a user seeking answers online, or collected in a Frequently Asked Questions (FAQ) document.

    References:
        https://schema.org/Question
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
    


class QuestionProperties(TypedDict):
    """A specific question - e.g. from a user seeking answers online, or collected in a Frequently Asked Questions (FAQ) document.

    References:
        https://schema.org/Question
    Note:
        Model Depth 4
    Attributes:
        acceptedAnswer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The answer(s) that has been accepted as best, typically on a Question/Answer site. Sites vary in their selection mechanisms, e.g. drawing on community opinion and/or the view of the Question author.
        suggestedAnswer: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An answer (possibly one of several, possibly incorrect) to a Question, e.g. on a Question/Answer site.
        answerCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The number of answers this question has received.
        eduQuestionType: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): For questions that are part of learning resources (e.g. Quiz), eduQuestionType indicates the format of question being given. Example: "Multiple choice", "Open ended", "Flashcard".
    """

    acceptedAnswer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    suggestedAnswer: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    answerCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    eduQuestionType: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#QuestionInheritedPropertiesTd = QuestionInheritedProperties()
#QuestionPropertiesTd = QuestionProperties()


class AllProperties(QuestionInheritedProperties , QuestionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[QuestionProperties, QuestionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Question"
    return model
    

Question = create_schema_org_model()