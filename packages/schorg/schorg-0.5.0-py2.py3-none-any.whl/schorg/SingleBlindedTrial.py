"""
A trial design in which the researcher knows which treatment the patient was randomly assigned to but the patient does not.

https://schema.org/SingleBlindedTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SingleBlindedTrialInheritedProperties(TypedDict):
    """A trial design in which the researcher knows which treatment the patient was randomly assigned to but the patient does not.

    References:
        https://schema.org/SingleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class SingleBlindedTrialProperties(TypedDict):
    """A trial design in which the researcher knows which treatment the patient was randomly assigned to but the patient does not.

    References:
        https://schema.org/SingleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#SingleBlindedTrialInheritedPropertiesTd = SingleBlindedTrialInheritedProperties()
#SingleBlindedTrialPropertiesTd = SingleBlindedTrialProperties()


class AllProperties(SingleBlindedTrialInheritedProperties , SingleBlindedTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SingleBlindedTrialProperties, SingleBlindedTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SingleBlindedTrial"
    return model
    

SingleBlindedTrial = create_schema_org_model()