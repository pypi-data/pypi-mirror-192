"""
Neurological system clinical examination.

https://schema.org/Neuro
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NeuroInheritedProperties(TypedDict):
    """Neurological system clinical examination.

    References:
        https://schema.org/Neuro
    Note:
        Model Depth 5
    Attributes:
    """

    


class NeuroProperties(TypedDict):
    """Neurological system clinical examination.

    References:
        https://schema.org/Neuro
    Note:
        Model Depth 5
    Attributes:
    """

    

#NeuroInheritedPropertiesTd = NeuroInheritedProperties()
#NeuroPropertiesTd = NeuroProperties()


class AllProperties(NeuroInheritedProperties , NeuroProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NeuroProperties, NeuroInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Neuro"
    return model
    

Neuro = create_schema_org_model()