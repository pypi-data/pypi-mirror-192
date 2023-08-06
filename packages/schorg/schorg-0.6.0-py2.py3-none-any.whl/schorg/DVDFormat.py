"""
DVDFormat.

https://schema.org/DVDFormat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DVDFormatInheritedProperties(TypedDict):
    """DVDFormat.

    References:
        https://schema.org/DVDFormat
    Note:
        Model Depth 5
    Attributes:
    """

    


class DVDFormatProperties(TypedDict):
    """DVDFormat.

    References:
        https://schema.org/DVDFormat
    Note:
        Model Depth 5
    Attributes:
    """

    

#DVDFormatInheritedPropertiesTd = DVDFormatInheritedProperties()
#DVDFormatPropertiesTd = DVDFormatProperties()


class AllProperties(DVDFormatInheritedProperties , DVDFormatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DVDFormatProperties, DVDFormatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DVDFormat"
    return model
    

DVDFormat = create_schema_org_model()