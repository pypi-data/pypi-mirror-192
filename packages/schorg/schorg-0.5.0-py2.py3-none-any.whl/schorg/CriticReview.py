"""
A [[CriticReview]] is a more specialized form of Review written or published by a source that is recognized for its reviewing activities. These can include online columns, travel and food guides, TV and radio shows, blogs and other independent Web sites. [[CriticReview]]s are typically more in-depth and professionally written. For simpler, casually written user/visitor/viewer/customer reviews, it is more appropriate to use the [[UserReview]] type. Review aggregator sites such as Metacritic already separate out the site's user reviews from selected critic reviews that originate from third-party sources.

https://schema.org/CriticReview
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CriticReviewInheritedProperties(TypedDict):
    """A [[CriticReview]] is a more specialized form of Review written or published by a source that is recognized for its reviewing activities. These can include online columns, travel and food guides, TV and radio shows, blogs and other independent Web sites. [[CriticReview]]s are typically more in-depth and professionally written. For simpler, casually written user/visitor/viewer/customer reviews, it is more appropriate to use the [[UserReview]] type. Review aggregator sites such as Metacritic already separate out the site's user reviews from selected critic reviews that originate from third-party sources.

    References:
        https://schema.org/CriticReview
    Note:
        Model Depth 4
    Attributes:
        reviewBody: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The actual body of the review.
        associatedMediaReview: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An associated [[MediaReview]], related by specific common content, topic or claim. The expectation is that this property would be most typically used in cases where a single activity is conducting both claim reviews and media reviews, in which case [[relatedMediaReview]] would commonly be used on a [[ClaimReview]], while [[relatedClaimReview]] would be used on [[MediaReview]].
        associatedReview: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An associated [[Review]].
        positiveNotes: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Provides positive considerations regarding something, for example product highlights or (alongside [[negativeNotes]]) pro/con lists for reviews.In the case of a [[Review]], the property describes the [[itemReviewed]] from the perspective of the review; in the case of a [[Product]], the product itself is being described.The property values can be expressed either as unstructured text (repeated as necessary), or if ordered, as a list (in which case the most positive is at the beginning of the list).
        reviewRating: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The rating given in this review. Note that reviews can themselves be rated. The ```reviewRating``` applies to rating given by the review. The [[aggregateRating]] property applies to the review itself, as a creative work.
        reviewAspect: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): This Review or Rating is relevant to this part or facet of the itemReviewed.
        itemReviewed: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The item that is being reviewed/rated.
        negativeNotes: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): Provides negative considerations regarding something, most typically in pro/con lists for reviews (alongside [[positiveNotes]]). For symmetry In the case of a [[Review]], the property describes the [[itemReviewed]] from the perspective of the review; in the case of a [[Product]], the product itself is being described. Since product descriptions tend to emphasise positive claims, it may be relatively unusual to find [[negativeNotes]] used in this way. Nevertheless for the sake of symmetry, [[negativeNotes]] can be used on [[Product]].The property values can be expressed either as unstructured text (repeated as necessary), or if ordered, as a list (in which case the most negative is at the beginning of the list).
        associatedClaimReview: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): An associated [[ClaimReview]], related by specific common content, topic or claim. The expectation is that this property would be most typically used in cases where a single activity is conducting both claim reviews and media reviews, in which case [[relatedMediaReview]] would commonly be used on a [[ClaimReview]], while [[relatedClaimReview]] would be used on [[MediaReview]].
    """

    reviewBody: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    associatedMediaReview: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    associatedReview: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    positiveNotes: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    reviewRating: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    reviewAspect: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    itemReviewed: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    negativeNotes: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    associatedClaimReview: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class CriticReviewProperties(TypedDict):
    """A [[CriticReview]] is a more specialized form of Review written or published by a source that is recognized for its reviewing activities. These can include online columns, travel and food guides, TV and radio shows, blogs and other independent Web sites. [[CriticReview]]s are typically more in-depth and professionally written. For simpler, casually written user/visitor/viewer/customer reviews, it is more appropriate to use the [[UserReview]] type. Review aggregator sites such as Metacritic already separate out the site's user reviews from selected critic reviews that originate from third-party sources.

    References:
        https://schema.org/CriticReview
    Note:
        Model Depth 4
    Attributes:
    """

    

#CriticReviewInheritedPropertiesTd = CriticReviewInheritedProperties()
#CriticReviewPropertiesTd = CriticReviewProperties()


class AllProperties(CriticReviewInheritedProperties , CriticReviewProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CriticReviewProperties, CriticReviewInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CriticReview"
    return model
    

CriticReview = create_schema_org_model()