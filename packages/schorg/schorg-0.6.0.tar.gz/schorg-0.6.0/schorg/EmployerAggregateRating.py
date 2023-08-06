"""
An aggregate rating of an Organization related to its role as an employer.

https://schema.org/EmployerAggregateRating
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EmployerAggregateRatingInheritedProperties(TypedDict):
    """An aggregate rating of an Organization related to its role as an employer.

    References:
        https://schema.org/EmployerAggregateRating
    Note:
        Model Depth 5
    Attributes:
        itemReviewed: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The item that is being reviewed/rated.
        ratingCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The count of total number of ratings.
        reviewCount: (Optional[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]): The count of total number of reviews.
    """

    itemReviewed: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    ratingCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    reviewCount: NotRequired[Union[List[Union[SchemaOrgObj, int, str]], SchemaOrgObj, int, str]]
    


class EmployerAggregateRatingProperties(TypedDict):
    """An aggregate rating of an Organization related to its role as an employer.

    References:
        https://schema.org/EmployerAggregateRating
    Note:
        Model Depth 5
    Attributes:
    """

    

#EmployerAggregateRatingInheritedPropertiesTd = EmployerAggregateRatingInheritedProperties()
#EmployerAggregateRatingPropertiesTd = EmployerAggregateRatingProperties()


class AllProperties(EmployerAggregateRatingInheritedProperties , EmployerAggregateRatingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EmployerAggregateRatingProperties, EmployerAggregateRatingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EmployerAggregateRating"
    return model
    

EmployerAggregateRating = create_schema_org_model()