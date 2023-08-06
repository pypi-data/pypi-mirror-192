"""
A publication containing information about varied topics that are pertinent to general information, a geographic area, or a specific subject matter (i.e. business, culture, education). Often published daily.

https://schema.org/Newspaper
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NewspaperInheritedProperties(TypedDict):
    """A publication containing information about varied topics that are pertinent to general information, a geographic area, or a specific subject matter (i.e. business, culture, education). Often published daily.

    References:
        https://schema.org/Newspaper
    Note:
        Model Depth 5
    Attributes:
    """

    


class NewspaperProperties(TypedDict):
    """A publication containing information about varied topics that are pertinent to general information, a geographic area, or a specific subject matter (i.e. business, culture, education). Often published daily.

    References:
        https://schema.org/Newspaper
    Note:
        Model Depth 5
    Attributes:
    """

    

#NewspaperInheritedPropertiesTd = NewspaperInheritedProperties()
#NewspaperPropertiesTd = NewspaperProperties()


class AllProperties(NewspaperInheritedProperties , NewspaperProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NewspaperProperties, NewspaperInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Newspaper"
    return model
    

Newspaper = create_schema_org_model()