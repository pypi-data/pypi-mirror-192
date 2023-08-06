"""
Physical activity that is engaged in to improve muscle and bone strength. Also referred to as resistance training.

https://schema.org/StrengthTraining
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class StrengthTrainingInheritedProperties(TypedDict):
    """Physical activity that is engaged in to improve muscle and bone strength. Also referred to as resistance training.

    References:
        https://schema.org/StrengthTraining
    Note:
        Model Depth 5
    Attributes:
    """

    


class StrengthTrainingProperties(TypedDict):
    """Physical activity that is engaged in to improve muscle and bone strength. Also referred to as resistance training.

    References:
        https://schema.org/StrengthTraining
    Note:
        Model Depth 5
    Attributes:
    """

    

#StrengthTrainingInheritedPropertiesTd = StrengthTrainingInheritedProperties()
#StrengthTrainingPropertiesTd = StrengthTrainingProperties()


class AllProperties(StrengthTrainingInheritedProperties , StrengthTrainingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[StrengthTrainingProperties, StrengthTrainingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "StrengthTraining"
    return model
    

StrengthTraining = create_schema_org_model()