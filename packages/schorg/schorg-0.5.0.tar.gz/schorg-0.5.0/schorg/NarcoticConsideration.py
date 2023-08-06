"""
Item is a narcotic as defined by the [1961 UN convention](https://www.incb.org/incb/en/narcotic-drugs/Yellowlist/yellow-list.html), for example marijuana or heroin.

https://schema.org/NarcoticConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NarcoticConsiderationInheritedProperties(TypedDict):
    """Item is a narcotic as defined by the [1961 UN convention](https://www.incb.org/incb/en/narcotic-drugs/Yellowlist/yellow-list.html), for example marijuana or heroin.

    References:
        https://schema.org/NarcoticConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class NarcoticConsiderationProperties(TypedDict):
    """Item is a narcotic as defined by the [1961 UN convention](https://www.incb.org/incb/en/narcotic-drugs/Yellowlist/yellow-list.html), for example marijuana or heroin.

    References:
        https://schema.org/NarcoticConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#NarcoticConsiderationInheritedPropertiesTd = NarcoticConsiderationInheritedProperties()
#NarcoticConsiderationPropertiesTd = NarcoticConsiderationProperties()


class AllProperties(NarcoticConsiderationInheritedProperties , NarcoticConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NarcoticConsiderationProperties, NarcoticConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NarcoticConsideration"
    return model
    

NarcoticConsideration = create_schema_org_model()