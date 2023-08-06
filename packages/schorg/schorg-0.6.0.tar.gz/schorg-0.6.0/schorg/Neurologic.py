"""
A specific branch of medical science that studies the nerves and nervous system and its respective disease states.

https://schema.org/Neurologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NeurologicInheritedProperties(TypedDict):
    """A specific branch of medical science that studies the nerves and nervous system and its respective disease states.

    References:
        https://schema.org/Neurologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class NeurologicProperties(TypedDict):
    """A specific branch of medical science that studies the nerves and nervous system and its respective disease states.

    References:
        https://schema.org/Neurologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#NeurologicInheritedPropertiesTd = NeurologicInheritedProperties()
#NeurologicPropertiesTd = NeurologicProperties()


class AllProperties(NeurologicInheritedProperties , NeurologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NeurologicProperties, NeurologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Neurologic"
    return model
    

Neurologic = create_schema_org_model()