"""
Classes of agents or pathogens that transmit infectious diseases. Enumerated type.

https://schema.org/InfectiousAgentClass
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InfectiousAgentClassInheritedProperties(TypedDict):
    """Classes of agents or pathogens that transmit infectious diseases. Enumerated type.

    References:
        https://schema.org/InfectiousAgentClass
    Note:
        Model Depth 5
    Attributes:
    """

    


class InfectiousAgentClassProperties(TypedDict):
    """Classes of agents or pathogens that transmit infectious diseases. Enumerated type.

    References:
        https://schema.org/InfectiousAgentClass
    Note:
        Model Depth 5
    Attributes:
    """

    

#InfectiousAgentClassInheritedPropertiesTd = InfectiousAgentClassInheritedProperties()
#InfectiousAgentClassPropertiesTd = InfectiousAgentClassProperties()


class AllProperties(InfectiousAgentClassInheritedProperties , InfectiousAgentClassProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InfectiousAgentClassProperties, InfectiousAgentClassInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InfectiousAgentClass"
    return model
    

InfectiousAgentClass = create_schema_org_model()