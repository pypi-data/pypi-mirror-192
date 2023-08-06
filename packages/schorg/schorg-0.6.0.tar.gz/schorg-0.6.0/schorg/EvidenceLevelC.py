"""
Only consensus opinion of experts, case studies, or standard-of-care.

https://schema.org/EvidenceLevelC
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EvidenceLevelCInheritedProperties(TypedDict):
    """Only consensus opinion of experts, case studies, or standard-of-care.

    References:
        https://schema.org/EvidenceLevelC
    Note:
        Model Depth 6
    Attributes:
    """

    


class EvidenceLevelCProperties(TypedDict):
    """Only consensus opinion of experts, case studies, or standard-of-care.

    References:
        https://schema.org/EvidenceLevelC
    Note:
        Model Depth 6
    Attributes:
    """

    

#EvidenceLevelCInheritedPropertiesTd = EvidenceLevelCInheritedProperties()
#EvidenceLevelCPropertiesTd = EvidenceLevelCProperties()


class AllProperties(EvidenceLevelCInheritedProperties , EvidenceLevelCProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EvidenceLevelCProperties, EvidenceLevelCInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EvidenceLevelC"
    return model
    

EvidenceLevelC = create_schema_org_model()