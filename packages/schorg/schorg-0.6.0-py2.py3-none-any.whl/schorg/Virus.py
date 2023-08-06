"""
Pathogenic virus that causes viral infection.

https://schema.org/Virus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VirusInheritedProperties(TypedDict):
    """Pathogenic virus that causes viral infection.

    References:
        https://schema.org/Virus
    Note:
        Model Depth 6
    Attributes:
    """

    


class VirusProperties(TypedDict):
    """Pathogenic virus that causes viral infection.

    References:
        https://schema.org/Virus
    Note:
        Model Depth 6
    Attributes:
    """

    

#VirusInheritedPropertiesTd = VirusInheritedProperties()
#VirusPropertiesTd = VirusProperties()


class AllProperties(VirusInheritedProperties , VirusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VirusProperties, VirusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Virus"
    return model
    

Virus = create_schema_org_model()