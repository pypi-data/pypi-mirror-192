"""
A date value in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).

https://schema.org/Date
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DateInheritedProperties(TypedDict):
    """A date value in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).

    References:
        https://schema.org/Date
    Note:
        Model Depth 5
    Attributes:
    """

    


class DateProperties(TypedDict):
    """A date value in [ISO 8601 date format](http://en.wikipedia.org/wiki/ISO_8601).

    References:
        https://schema.org/Date
    Note:
        Model Depth 5
    Attributes:
    """

    

#DateInheritedPropertiesTd = DateInheritedProperties()
#DatePropertiesTd = DateProperties()


class AllProperties(DateInheritedProperties , DateProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DateProperties, DateInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Date"
    return model
    

Date = create_schema_org_model()