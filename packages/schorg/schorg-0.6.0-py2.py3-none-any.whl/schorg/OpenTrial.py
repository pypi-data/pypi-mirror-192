"""
A trial design in which the researcher knows the full details of the treatment, and so does the patient.

https://schema.org/OpenTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OpenTrialInheritedProperties(TypedDict):
    """A trial design in which the researcher knows the full details of the treatment, and so does the patient.

    References:
        https://schema.org/OpenTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class OpenTrialProperties(TypedDict):
    """A trial design in which the researcher knows the full details of the treatment, and so does the patient.

    References:
        https://schema.org/OpenTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#OpenTrialInheritedPropertiesTd = OpenTrialInheritedProperties()
#OpenTrialPropertiesTd = OpenTrialProperties()


class AllProperties(OpenTrialInheritedProperties , OpenTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OpenTrialProperties, OpenTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OpenTrial"
    return model
    

OpenTrial = create_schema_org_model()