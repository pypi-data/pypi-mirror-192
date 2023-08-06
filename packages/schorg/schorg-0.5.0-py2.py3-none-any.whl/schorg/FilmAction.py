"""
The act of capturing sound and moving images on film, video, or digitally.

https://schema.org/FilmAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class FilmActionInheritedProperties(TypedDict):
    """The act of capturing sound and moving images on film, video, or digitally.

    References:
        https://schema.org/FilmAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class FilmActionProperties(TypedDict):
    """The act of capturing sound and moving images on film, video, or digitally.

    References:
        https://schema.org/FilmAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#FilmActionInheritedPropertiesTd = FilmActionInheritedProperties()
#FilmActionPropertiesTd = FilmActionProperties()


class AllProperties(FilmActionInheritedProperties , FilmActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[FilmActionProperties, FilmActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "FilmAction"
    return model
    

FilmAction = create_schema_org_model()