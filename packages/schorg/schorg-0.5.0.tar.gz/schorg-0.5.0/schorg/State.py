"""
A state or province of a country.

https://schema.org/State
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class StateInheritedProperties(TypedDict):
    """A state or province of a country.

    References:
        https://schema.org/State
    Note:
        Model Depth 4
    Attributes:
    """

    


class StateProperties(TypedDict):
    """A state or province of a country.

    References:
        https://schema.org/State
    Note:
        Model Depth 4
    Attributes:
    """

    

#StateInheritedPropertiesTd = StateInheritedProperties()
#StatePropertiesTd = StateProperties()


class AllProperties(StateInheritedProperties , StateProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[StateProperties, StateInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "State"
    return model
    

State = create_schema_org_model()