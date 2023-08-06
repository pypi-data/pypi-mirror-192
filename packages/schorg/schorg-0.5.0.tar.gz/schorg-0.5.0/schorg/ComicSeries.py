"""
A sequential publication of comic stories under a    	unifying title, for example "The Amazing Spider-Man" or "Groo the    	Wanderer".

https://schema.org/ComicSeries
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ComicSeriesInheritedProperties(TypedDict):
    """A sequential publication of comic stories under a    	unifying title, for example "The Amazing Spider-Man" or "Groo the    	Wanderer".

    References:
        https://schema.org/ComicSeries
    Note:
        Model Depth 5
    Attributes:
    """

    


class ComicSeriesProperties(TypedDict):
    """A sequential publication of comic stories under a    	unifying title, for example "The Amazing Spider-Man" or "Groo the    	Wanderer".

    References:
        https://schema.org/ComicSeries
    Note:
        Model Depth 5
    Attributes:
    """

    

#ComicSeriesInheritedPropertiesTd = ComicSeriesInheritedProperties()
#ComicSeriesPropertiesTd = ComicSeriesProperties()


class AllProperties(ComicSeriesInheritedProperties , ComicSeriesProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ComicSeriesProperties, ComicSeriesInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ComicSeries"
    return model
    

ComicSeries = create_schema_org_model()