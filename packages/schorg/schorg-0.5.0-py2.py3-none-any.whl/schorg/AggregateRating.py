"""
The average rating based on multiple ratings or reviews.

https://schema.org/AggregateRating
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AggregateRatingInheritedProperties(TypedDict):
    """The average rating based on multiple ratings or reviews.

    References:
        https://schema.org/AggregateRating
    Note:
        Model Depth 4
    Attributes:
        reviewAspect: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): This Review or Rating is relevant to this part or facet of the itemReviewed.
        author: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The author of this content or rating. Please note that author is special in that HTML 5 provides a special mechanism for indicating authorship via the rel tag. That is equivalent to this and may be used interchangeably.
        ratingExplanation: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A short explanation (e.g. one to two sentences) providing background context and other information that led to the conclusion expressed in the rating. This is particularly applicable to ratings associated with "fact check" markup using [[ClaimReview]].
        bestRating: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The highest value allowed in this rating system. If bestRating is omitted, 5 is assumed.
        ratingValue: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The rating for the content.Usage guidelines:* Use values from 0123456789 (Unicode 'DIGIT ZERO' (U+0030) to 'DIGIT NINE' (U+0039)) rather than superficially similar Unicode symbols.* Use '.' (Unicode 'FULL STOP' (U+002E)) rather than ',' to indicate a decimal point. Avoid using these symbols as a readability separator.
        worstRating: (Optional[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]): The lowest value allowed in this rating system. If worstRating is omitted, 1 is assumed.
    """

    reviewAspect: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    author: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    ratingExplanation: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    bestRating: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    ratingValue: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    worstRating: NotRequired[Union[List[Union[SchemaOrgObj, str, StrictInt, StrictFloat]], SchemaOrgObj, str, StrictInt, StrictFloat]]
    


class AggregateRatingProperties(TypedDict):
    """The average rating based on multiple ratings or reviews.

    References:
        https://schema.org/AggregateRating
    Note:
        Model Depth 4
    Attributes:
        itemReviewed: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The item that is being reviewed/rated.
        ratingCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The count of total number of ratings.
        reviewCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The count of total number of reviews.
    """

    itemReviewed: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    ratingCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    reviewCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    

#AggregateRatingInheritedPropertiesTd = AggregateRatingInheritedProperties()
#AggregateRatingPropertiesTd = AggregateRatingProperties()


class AllProperties(AggregateRatingInheritedProperties , AggregateRatingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AggregateRatingProperties, AggregateRatingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AggregateRating"
    return model
    

AggregateRating = create_schema_org_model()