"""
Musculoskeletal system clinical examination.

https://schema.org/MusculoskeletalExam
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MusculoskeletalExamInheritedProperties(TypedDict):
    """Musculoskeletal system clinical examination.

    References:
        https://schema.org/MusculoskeletalExam
    Note:
        Model Depth 5
    Attributes:
    """

    


class MusculoskeletalExamProperties(TypedDict):
    """Musculoskeletal system clinical examination.

    References:
        https://schema.org/MusculoskeletalExam
    Note:
        Model Depth 5
    Attributes:
    """

    

#MusculoskeletalExamInheritedPropertiesTd = MusculoskeletalExamInheritedProperties()
#MusculoskeletalExamPropertiesTd = MusculoskeletalExamProperties()


class AllProperties(MusculoskeletalExamInheritedProperties , MusculoskeletalExamProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MusculoskeletalExamProperties, MusculoskeletalExamInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MusculoskeletalExam"
    return model
    

MusculoskeletalExam = create_schema_org_model()