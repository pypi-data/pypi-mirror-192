"""
A specific branch of medical science that pertains to the study of the respiratory system and its respective disease states.

https://schema.org/Pulmonary
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PulmonaryInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to the study of the respiratory system and its respective disease states.

    References:
        https://schema.org/Pulmonary
    Note:
        Model Depth 6
    Attributes:
    """

    


class PulmonaryProperties(TypedDict):
    """A specific branch of medical science that pertains to the study of the respiratory system and its respective disease states.

    References:
        https://schema.org/Pulmonary
    Note:
        Model Depth 6
    Attributes:
    """

    

#PulmonaryInheritedPropertiesTd = PulmonaryInheritedProperties()
#PulmonaryPropertiesTd = PulmonaryProperties()


class AllProperties(PulmonaryInheritedProperties , PulmonaryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PulmonaryProperties, PulmonaryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Pulmonary"
    return model
    

Pulmonary = create_schema_org_model()