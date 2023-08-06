"""
Information about questions that may be asked, when to see a professional, measures before seeing a doctor or content about the first consultation.

https://schema.org/SeeDoctorHealthAspect
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SeeDoctorHealthAspectInheritedProperties(TypedDict):
    """Information about questions that may be asked, when to see a professional, measures before seeing a doctor or content about the first consultation.

    References:
        https://schema.org/SeeDoctorHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    


class SeeDoctorHealthAspectProperties(TypedDict):
    """Information about questions that may be asked, when to see a professional, measures before seeing a doctor or content about the first consultation.

    References:
        https://schema.org/SeeDoctorHealthAspect
    Note:
        Model Depth 5
    Attributes:
    """

    

#SeeDoctorHealthAspectInheritedPropertiesTd = SeeDoctorHealthAspectInheritedProperties()
#SeeDoctorHealthAspectPropertiesTd = SeeDoctorHealthAspectProperties()


class AllProperties(SeeDoctorHealthAspectInheritedProperties , SeeDoctorHealthAspectProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SeeDoctorHealthAspectProperties, SeeDoctorHealthAspectInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SeeDoctorHealthAspect"
    return model
    

SeeDoctorHealthAspect = create_schema_org_model()