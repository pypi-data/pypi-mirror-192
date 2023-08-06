"""
A mosque.

https://schema.org/Mosque
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MosqueInheritedProperties(TypedDict):
    """A mosque.

    References:
        https://schema.org/Mosque
    Note:
        Model Depth 5
    Attributes:
    """

    


class MosqueProperties(TypedDict):
    """A mosque.

    References:
        https://schema.org/Mosque
    Note:
        Model Depth 5
    Attributes:
    """

    

#MosqueInheritedPropertiesTd = MosqueInheritedProperties()
#MosquePropertiesTd = MosqueProperties()


class AllProperties(MosqueInheritedProperties , MosqueProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MosqueProperties, MosqueInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Mosque"
    return model
    

Mosque = create_schema_org_model()