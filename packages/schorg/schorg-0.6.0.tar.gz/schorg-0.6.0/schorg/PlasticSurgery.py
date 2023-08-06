"""
A specific branch of medical science that pertains to therapeutic or cosmetic repair or re-formation of missing, injured or malformed tissues or body parts by manual and instrumental means.

https://schema.org/PlasticSurgery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PlasticSurgeryInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to therapeutic or cosmetic repair or re-formation of missing, injured or malformed tissues or body parts by manual and instrumental means.

    References:
        https://schema.org/PlasticSurgery
    Note:
        Model Depth 5
    Attributes:
    """

    


class PlasticSurgeryProperties(TypedDict):
    """A specific branch of medical science that pertains to therapeutic or cosmetic repair or re-formation of missing, injured or malformed tissues or body parts by manual and instrumental means.

    References:
        https://schema.org/PlasticSurgery
    Note:
        Model Depth 5
    Attributes:
    """

    

#PlasticSurgeryInheritedPropertiesTd = PlasticSurgeryInheritedProperties()
#PlasticSurgeryPropertiesTd = PlasticSurgeryProperties()


class AllProperties(PlasticSurgeryInheritedProperties , PlasticSurgeryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PlasticSurgeryProperties, PlasticSurgeryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PlasticSurgery"
    return model
    

PlasticSurgery = create_schema_org_model()