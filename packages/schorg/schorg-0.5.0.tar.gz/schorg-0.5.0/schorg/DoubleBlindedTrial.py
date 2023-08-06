"""
A trial design in which neither the researcher nor the patient knows the details of the treatment the patient was randomly assigned to.

https://schema.org/DoubleBlindedTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DoubleBlindedTrialInheritedProperties(TypedDict):
    """A trial design in which neither the researcher nor the patient knows the details of the treatment the patient was randomly assigned to.

    References:
        https://schema.org/DoubleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class DoubleBlindedTrialProperties(TypedDict):
    """A trial design in which neither the researcher nor the patient knows the details of the treatment the patient was randomly assigned to.

    References:
        https://schema.org/DoubleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#DoubleBlindedTrialInheritedPropertiesTd = DoubleBlindedTrialInheritedProperties()
#DoubleBlindedTrialPropertiesTd = DoubleBlindedTrialProperties()


class AllProperties(DoubleBlindedTrialInheritedProperties , DoubleBlindedTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DoubleBlindedTrialProperties, DoubleBlindedTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DoubleBlindedTrial"
    return model
    

DoubleBlindedTrial = create_schema_org_model()