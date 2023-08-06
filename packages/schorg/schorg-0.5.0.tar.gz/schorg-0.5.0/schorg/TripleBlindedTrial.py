"""
A trial design in which neither the researcher, the person administering the therapy nor the patient knows the details of the treatment the patient was randomly assigned to.

https://schema.org/TripleBlindedTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TripleBlindedTrialInheritedProperties(TypedDict):
    """A trial design in which neither the researcher, the person administering the therapy nor the patient knows the details of the treatment the patient was randomly assigned to.

    References:
        https://schema.org/TripleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class TripleBlindedTrialProperties(TypedDict):
    """A trial design in which neither the researcher, the person administering the therapy nor the patient knows the details of the treatment the patient was randomly assigned to.

    References:
        https://schema.org/TripleBlindedTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#TripleBlindedTrialInheritedPropertiesTd = TripleBlindedTrialInheritedProperties()
#TripleBlindedTrialPropertiesTd = TripleBlindedTrialProperties()


class AllProperties(TripleBlindedTrialInheritedProperties , TripleBlindedTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TripleBlindedTrialProperties, TripleBlindedTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TripleBlindedTrial"
    return model
    

TripleBlindedTrial = create_schema_org_model()