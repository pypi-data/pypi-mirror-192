"""
Positron emission tomography imaging.

https://schema.org/PET
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PETInheritedProperties(TypedDict):
    """Positron emission tomography imaging.

    References:
        https://schema.org/PET
    Note:
        Model Depth 6
    Attributes:
    """

    


class PETProperties(TypedDict):
    """Positron emission tomography imaging.

    References:
        https://schema.org/PET
    Note:
        Model Depth 6
    Attributes:
    """

    

#PETInheritedPropertiesTd = PETInheritedProperties()
#PETPropertiesTd = PETProperties()


class AllProperties(PETInheritedProperties , PETProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PETProperties, PETInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PET"
    return model
    

PET = create_schema_org_model()