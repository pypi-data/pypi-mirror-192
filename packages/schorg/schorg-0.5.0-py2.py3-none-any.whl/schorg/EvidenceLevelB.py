"""
Data derived from a single randomized trial, or nonrandomized studies.

https://schema.org/EvidenceLevelB
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EvidenceLevelBInheritedProperties(TypedDict):
    """Data derived from a single randomized trial, or nonrandomized studies.

    References:
        https://schema.org/EvidenceLevelB
    Note:
        Model Depth 6
    Attributes:
    """

    


class EvidenceLevelBProperties(TypedDict):
    """Data derived from a single randomized trial, or nonrandomized studies.

    References:
        https://schema.org/EvidenceLevelB
    Note:
        Model Depth 6
    Attributes:
    """

    

#EvidenceLevelBInheritedPropertiesTd = EvidenceLevelBInheritedProperties()
#EvidenceLevelBPropertiesTd = EvidenceLevelBProperties()


class AllProperties(EvidenceLevelBInheritedProperties , EvidenceLevelBProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EvidenceLevelBProperties, EvidenceLevelBInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EvidenceLevelB"
    return model
    

EvidenceLevelB = create_schema_org_model()