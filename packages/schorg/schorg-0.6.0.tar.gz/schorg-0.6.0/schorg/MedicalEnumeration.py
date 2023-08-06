"""
Enumerations related to health and the practice of medicine: A concept that is used to attribute a quality to another concept, as a qualifier, a collection of items or a listing of all of the elements of a set in medicine practice.

https://schema.org/MedicalEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MedicalEnumerationInheritedProperties(TypedDict):
    """Enumerations related to health and the practice of medicine: A concept that is used to attribute a quality to another concept, as a qualifier, a collection of items or a listing of all of the elements of a set in medicine practice.

    References:
        https://schema.org/MedicalEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MedicalEnumerationProperties(TypedDict):
    """Enumerations related to health and the practice of medicine: A concept that is used to attribute a quality to another concept, as a qualifier, a collection of items or a listing of all of the elements of a set in medicine practice.

    References:
        https://schema.org/MedicalEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#MedicalEnumerationInheritedPropertiesTd = MedicalEnumerationInheritedProperties()
#MedicalEnumerationPropertiesTd = MedicalEnumerationProperties()


class AllProperties(MedicalEnumerationInheritedProperties , MedicalEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MedicalEnumerationProperties, MedicalEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MedicalEnumeration"
    return model
    

MedicalEnumeration = create_schema_org_model()