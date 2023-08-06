"""
CassetteFormat.

https://schema.org/CassetteFormat
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CassetteFormatInheritedProperties(TypedDict):
    """CassetteFormat.

    References:
        https://schema.org/CassetteFormat
    Note:
        Model Depth 5
    Attributes:
    """

    


class CassetteFormatProperties(TypedDict):
    """CassetteFormat.

    References:
        https://schema.org/CassetteFormat
    Note:
        Model Depth 5
    Attributes:
    """

    

#CassetteFormatInheritedPropertiesTd = CassetteFormatInheritedProperties()
#CassetteFormatPropertiesTd = CassetteFormatProperties()


class AllProperties(CassetteFormatInheritedProperties , CassetteFormatProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CassetteFormatProperties, CassetteFormatInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CassetteFormat"
    return model
    

CassetteFormat = create_schema_org_model()