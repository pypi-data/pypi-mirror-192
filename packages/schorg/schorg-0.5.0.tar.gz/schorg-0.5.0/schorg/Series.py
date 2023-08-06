"""
A Series in schema.org is a group of related items, typically but not necessarily of the same kind. See also [[CreativeWorkSeries]], [[EventSeries]].

https://schema.org/Series
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SeriesInheritedProperties(TypedDict):
    """A Series in schema.org is a group of related items, typically but not necessarily of the same kind. See also [[CreativeWorkSeries]], [[EventSeries]].

    References:
        https://schema.org/Series
    Note:
        Model Depth 3
    Attributes:
    """

    


class SeriesProperties(TypedDict):
    """A Series in schema.org is a group of related items, typically but not necessarily of the same kind. See also [[CreativeWorkSeries]], [[EventSeries]].

    References:
        https://schema.org/Series
    Note:
        Model Depth 3
    Attributes:
    """

    

#SeriesInheritedPropertiesTd = SeriesInheritedProperties()
#SeriesPropertiesTd = SeriesProperties()


class AllProperties(SeriesInheritedProperties , SeriesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SeriesProperties, SeriesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Series"
    return model
    

Series = create_schema_org_model()