"""
A specific branch of medical science that pertains to treating diseases, injuries and deformities by manual and instrumental means.

https://schema.org/Surgical
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SurgicalInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to treating diseases, injuries and deformities by manual and instrumental means.

    References:
        https://schema.org/Surgical
    Note:
        Model Depth 6
    Attributes:
    """

    


class SurgicalProperties(TypedDict):
    """A specific branch of medical science that pertains to treating diseases, injuries and deformities by manual and instrumental means.

    References:
        https://schema.org/Surgical
    Note:
        Model Depth 6
    Attributes:
    """

    

#SurgicalInheritedPropertiesTd = SurgicalInheritedProperties()
#SurgicalPropertiesTd = SurgicalProperties()


class AllProperties(SurgicalInheritedProperties , SurgicalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SurgicalProperties, SurgicalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Surgical"
    return model
    

Surgical = create_schema_org_model()