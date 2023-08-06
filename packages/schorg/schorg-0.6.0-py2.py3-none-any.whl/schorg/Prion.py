"""
A prion is an infectious agent composed of protein in a misfolded form.

https://schema.org/Prion
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PrionInheritedProperties(TypedDict):
    """A prion is an infectious agent composed of protein in a misfolded form.

    References:
        https://schema.org/Prion
    Note:
        Model Depth 6
    Attributes:
    """

    


class PrionProperties(TypedDict):
    """A prion is an infectious agent composed of protein in a misfolded form.

    References:
        https://schema.org/Prion
    Note:
        Model Depth 6
    Attributes:
    """

    

#PrionInheritedPropertiesTd = PrionInheritedProperties()
#PrionPropertiesTd = PrionProperties()


class AllProperties(PrionInheritedProperties , PrionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PrionProperties, PrionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Prion"
    return model
    

Prion = create_schema_org_model()