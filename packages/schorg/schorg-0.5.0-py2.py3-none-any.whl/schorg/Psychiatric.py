"""
A specific branch of medical science that is concerned with the study, treatment, and prevention of mental illness, using both medical and psychological therapies.

https://schema.org/Psychiatric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PsychiatricInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with the study, treatment, and prevention of mental illness, using both medical and psychological therapies.

    References:
        https://schema.org/Psychiatric
    Note:
        Model Depth 5
    Attributes:
    """

    


class PsychiatricProperties(TypedDict):
    """A specific branch of medical science that is concerned with the study, treatment, and prevention of mental illness, using both medical and psychological therapies.

    References:
        https://schema.org/Psychiatric
    Note:
        Model Depth 5
    Attributes:
    """

    

#PsychiatricInheritedPropertiesTd = PsychiatricInheritedProperties()
#PsychiatricPropertiesTd = PsychiatricProperties()


class AllProperties(PsychiatricInheritedProperties , PsychiatricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PsychiatricProperties, PsychiatricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Psychiatric"
    return model
    

Psychiatric = create_schema_org_model()