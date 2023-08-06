"""
Quantity: Duration (use [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601)).

https://schema.org/Duration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DurationInheritedProperties(TypedDict):
    """Quantity: Duration (use [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601)).

    References:
        https://schema.org/Duration
    Note:
        Model Depth 4
    Attributes:
    """

    


class DurationProperties(TypedDict):
    """Quantity: Duration (use [ISO 8601 duration format](http://en.wikipedia.org/wiki/ISO_8601)).

    References:
        https://schema.org/Duration
    Note:
        Model Depth 4
    Attributes:
    """

    

#DurationInheritedPropertiesTd = DurationInheritedProperties()
#DurationPropertiesTd = DurationProperties()


class AllProperties(DurationInheritedProperties , DurationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DurationProperties, DurationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Duration"
    return model
    

Duration = create_schema_org_model()