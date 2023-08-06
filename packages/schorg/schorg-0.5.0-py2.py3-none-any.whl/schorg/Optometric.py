"""
The science or practice of testing visual acuity and prescribing corrective lenses.

https://schema.org/Optometric
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OptometricInheritedProperties(TypedDict):
    """The science or practice of testing visual acuity and prescribing corrective lenses.

    References:
        https://schema.org/Optometric
    Note:
        Model Depth 5
    Attributes:
    """

    


class OptometricProperties(TypedDict):
    """The science or practice of testing visual acuity and prescribing corrective lenses.

    References:
        https://schema.org/Optometric
    Note:
        Model Depth 5
    Attributes:
    """

    

#OptometricInheritedPropertiesTd = OptometricInheritedProperties()
#OptometricPropertiesTd = OptometricProperties()


class AllProperties(OptometricInheritedProperties , OptometricProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OptometricProperties, OptometricInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Optometric"
    return model
    

Optometric = create_schema_org_model()