"""
A specific branch of medical science that is concerned with the study of the cause, origin and nature of a disease state, including its consequences as a result of manifestation of the disease. In clinical care, the term is used to designate a branch of medicine using laboratory tests to diagnose and determine the prognostic significance of illness.

https://schema.org/Pathology
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PathologyInheritedProperties(TypedDict):
    """A specific branch of medical science that is concerned with the study of the cause, origin and nature of a disease state, including its consequences as a result of manifestation of the disease. In clinical care, the term is used to designate a branch of medicine using laboratory tests to diagnose and determine the prognostic significance of illness.

    References:
        https://schema.org/Pathology
    Note:
        Model Depth 6
    Attributes:
    """

    


class PathologyProperties(TypedDict):
    """A specific branch of medical science that is concerned with the study of the cause, origin and nature of a disease state, including its consequences as a result of manifestation of the disease. In clinical care, the term is used to designate a branch of medicine using laboratory tests to diagnose and determine the prognostic significance of illness.

    References:
        https://schema.org/Pathology
    Note:
        Model Depth 6
    Attributes:
    """

    

#PathologyInheritedPropertiesTd = PathologyInheritedProperties()
#PathologyPropertiesTd = PathologyProperties()


class AllProperties(PathologyInheritedProperties , PathologyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PathologyProperties, PathologyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Pathology"
    return model
    

Pathology = create_schema_org_model()