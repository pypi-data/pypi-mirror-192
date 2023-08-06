"""
A roofing contractor.

https://schema.org/RoofingContractor
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RoofingContractorInheritedProperties(TypedDict):
    """A roofing contractor.

    References:
        https://schema.org/RoofingContractor
    Note:
        Model Depth 5
    Attributes:
    """

    


class RoofingContractorProperties(TypedDict):
    """A roofing contractor.

    References:
        https://schema.org/RoofingContractor
    Note:
        Model Depth 5
    Attributes:
    """

    

#RoofingContractorInheritedPropertiesTd = RoofingContractorInheritedProperties()
#RoofingContractorPropertiesTd = RoofingContractorProperties()


class AllProperties(RoofingContractorInheritedProperties , RoofingContractorProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RoofingContractorProperties, RoofingContractorInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "RoofingContractor"
    return model
    

RoofingContractor = create_schema_org_model()