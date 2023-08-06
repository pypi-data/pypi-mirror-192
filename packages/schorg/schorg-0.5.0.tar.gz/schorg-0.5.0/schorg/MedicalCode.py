"""
A code for a medical entity.

https://schema.org/MedicalCode
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalCodeInheritedProperties(TypedDict):
    """A code for a medical entity.

    References:
        https://schema.org/MedicalCode
    Note:
        Model Depth 4
    Attributes:
        codeValue: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A short textual code that uniquely identifies the value.
        inCodeSet: (Optional[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]): A [[CategoryCodeSet]] that contains this category code.
    """

    codeValue: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    inCodeSet: NotRequired[Union[List[Union[SchemaOrgObj, str, AnyUrl]], SchemaOrgObj, str, AnyUrl]]
    


class MedicalCodeProperties(TypedDict):
    """A code for a medical entity.

    References:
        https://schema.org/MedicalCode
    Note:
        Model Depth 4
    Attributes:
        codeValue: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): A short textual code that uniquely identifies the value.
        codingSystem: (Optional[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]): The coding system, e.g. 'ICD-10'.
    """

    codeValue: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    codingSystem: NotRequired[Union[List[Union[str, SchemaOrgObj]], str, SchemaOrgObj]]
    

#MedicalCodeInheritedPropertiesTd = MedicalCodeInheritedProperties()
#MedicalCodePropertiesTd = MedicalCodeProperties()


class AllProperties(MedicalCodeInheritedProperties , MedicalCodeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalCodeProperties, MedicalCodeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalCode"
    return model
    

MedicalCode = create_schema_org_model()