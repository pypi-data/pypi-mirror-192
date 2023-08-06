"""
A health profession of a person formally educated and trained in the care of the sick or infirm person.

https://schema.org/Nursing
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NursingInheritedProperties(TypedDict):
    """A health profession of a person formally educated and trained in the care of the sick or infirm person.

    References:
        https://schema.org/Nursing
    Note:
        Model Depth 5
    Attributes:
    """

    


class NursingProperties(TypedDict):
    """A health profession of a person formally educated and trained in the care of the sick or infirm person.

    References:
        https://schema.org/Nursing
    Note:
        Model Depth 5
    Attributes:
    """

    

#NursingInheritedPropertiesTd = NursingInheritedProperties()
#NursingPropertiesTd = NursingProperties()


class AllProperties(NursingInheritedProperties , NursingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NursingProperties, NursingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nursing"
    return model
    

Nursing = create_schema_org_model()