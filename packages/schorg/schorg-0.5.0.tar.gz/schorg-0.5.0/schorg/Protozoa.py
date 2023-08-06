"""
Single-celled organism that causes an infection.

https://schema.org/Protozoa
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ProtozoaInheritedProperties(TypedDict):
    """Single-celled organism that causes an infection.

    References:
        https://schema.org/Protozoa
    Note:
        Model Depth 6
    Attributes:
    """

    


class ProtozoaProperties(TypedDict):
    """Single-celled organism that causes an infection.

    References:
        https://schema.org/Protozoa
    Note:
        Model Depth 6
    Attributes:
    """

    

#ProtozoaInheritedPropertiesTd = ProtozoaInheritedProperties()
#ProtozoaPropertiesTd = ProtozoaProperties()


class AllProperties(ProtozoaInheritedProperties , ProtozoaProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ProtozoaProperties, ProtozoaInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Protozoa"
    return model
    

Protozoa = create_schema_org_model()