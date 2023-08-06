"""
A general code for cases where relevance to children is reduced, e.g. adult education, mortgages, retirement-related products, etc.

https://schema.org/ReducedRelevanceForChildrenConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReducedRelevanceForChildrenConsiderationInheritedProperties(TypedDict):
    """A general code for cases where relevance to children is reduced, e.g. adult education, mortgages, retirement-related products, etc.

    References:
        https://schema.org/ReducedRelevanceForChildrenConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReducedRelevanceForChildrenConsiderationProperties(TypedDict):
    """A general code for cases where relevance to children is reduced, e.g. adult education, mortgages, retirement-related products, etc.

    References:
        https://schema.org/ReducedRelevanceForChildrenConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReducedRelevanceForChildrenConsiderationInheritedPropertiesTd = ReducedRelevanceForChildrenConsiderationInheritedProperties()
#ReducedRelevanceForChildrenConsiderationPropertiesTd = ReducedRelevanceForChildrenConsiderationProperties()


class AllProperties(ReducedRelevanceForChildrenConsiderationInheritedProperties , ReducedRelevanceForChildrenConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReducedRelevanceForChildrenConsiderationProperties, ReducedRelevanceForChildrenConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReducedRelevanceForChildrenConsideration"
    return model
    

ReducedRelevanceForChildrenConsideration = create_schema_org_model()