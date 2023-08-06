"""
Cardiovascular system assessment with clinical examination.

https://schema.org/CardiovascularExam
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CardiovascularExamInheritedProperties(TypedDict):
    """Cardiovascular system assessment with clinical examination.

    References:
        https://schema.org/CardiovascularExam
    Note:
        Model Depth 5
    Attributes:
    """

    


class CardiovascularExamProperties(TypedDict):
    """Cardiovascular system assessment with clinical examination.

    References:
        https://schema.org/CardiovascularExam
    Note:
        Model Depth 5
    Attributes:
    """

    

#CardiovascularExamInheritedPropertiesTd = CardiovascularExamInheritedProperties()
#CardiovascularExamPropertiesTd = CardiovascularExamProperties()


class AllProperties(CardiovascularExamInheritedProperties , CardiovascularExamProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CardiovascularExamProperties, CardiovascularExamInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CardiovascularExam"
    return model
    

CardiovascularExam = create_schema_org_model()