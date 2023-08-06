"""
A gym.

https://schema.org/ExerciseGym
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ExerciseGymInheritedProperties(TypedDict):
    """A gym.

    References:
        https://schema.org/ExerciseGym
    Note:
        Model Depth 5
    Attributes:
    """

    


class ExerciseGymProperties(TypedDict):
    """A gym.

    References:
        https://schema.org/ExerciseGym
    Note:
        Model Depth 5
    Attributes:
    """

    

#ExerciseGymInheritedPropertiesTd = ExerciseGymInheritedProperties()
#ExerciseGymPropertiesTd = ExerciseGymProperties()


class AllProperties(ExerciseGymInheritedProperties , ExerciseGymProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ExerciseGymProperties, ExerciseGymInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ExerciseGym"
    return model
    

ExerciseGym = create_schema_org_model()