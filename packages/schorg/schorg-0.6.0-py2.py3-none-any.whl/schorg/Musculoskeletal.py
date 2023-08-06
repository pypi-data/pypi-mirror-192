"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of muscles, ligaments and skeletal system.

https://schema.org/Musculoskeletal
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusculoskeletalInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of muscles, ligaments and skeletal system.

    References:
        https://schema.org/Musculoskeletal
    Note:
        Model Depth 6
    Attributes:
    """

    


class MusculoskeletalProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of muscles, ligaments and skeletal system.

    References:
        https://schema.org/Musculoskeletal
    Note:
        Model Depth 6
    Attributes:
    """

    

#MusculoskeletalInheritedPropertiesTd = MusculoskeletalInheritedProperties()
#MusculoskeletalPropertiesTd = MusculoskeletalProperties()


class AllProperties(MusculoskeletalInheritedProperties , MusculoskeletalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusculoskeletalProperties, MusculoskeletalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Musculoskeletal"
    return model
    

Musculoskeletal = create_schema_org_model()