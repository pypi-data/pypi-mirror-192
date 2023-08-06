"""
An international trial.

https://schema.org/InternationalTrial
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InternationalTrialInheritedProperties(TypedDict):
    """An international trial.

    References:
        https://schema.org/InternationalTrial
    Note:
        Model Depth 6
    Attributes:
    """

    


class InternationalTrialProperties(TypedDict):
    """An international trial.

    References:
        https://schema.org/InternationalTrial
    Note:
        Model Depth 6
    Attributes:
    """

    

#InternationalTrialInheritedPropertiesTd = InternationalTrialInheritedProperties()
#InternationalTrialPropertiesTd = InternationalTrialProperties()


class AllProperties(InternationalTrialInheritedProperties , InternationalTrialProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InternationalTrialProperties, InternationalTrialInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InternationalTrial"
    return model
    

InternationalTrial = create_schema_org_model()