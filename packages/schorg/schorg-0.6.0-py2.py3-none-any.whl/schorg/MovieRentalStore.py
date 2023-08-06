"""
A movie rental store.

https://schema.org/MovieRentalStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MovieRentalStoreInheritedProperties(TypedDict):
    """A movie rental store.

    References:
        https://schema.org/MovieRentalStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class MovieRentalStoreProperties(TypedDict):
    """A movie rental store.

    References:
        https://schema.org/MovieRentalStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#MovieRentalStoreInheritedPropertiesTd = MovieRentalStoreInheritedProperties()
#MovieRentalStorePropertiesTd = MovieRentalStoreProperties()


class AllProperties(MovieRentalStoreInheritedProperties , MovieRentalStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MovieRentalStoreProperties, MovieRentalStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MovieRentalStore"
    return model
    

MovieRentalStore = create_schema_org_model()