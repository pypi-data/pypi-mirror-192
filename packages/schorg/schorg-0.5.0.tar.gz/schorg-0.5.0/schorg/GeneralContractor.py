"""
A general contractor.

https://schema.org/GeneralContractor
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GeneralContractorInheritedProperties(TypedDict):
    """A general contractor.

    References:
        https://schema.org/GeneralContractor
    Note:
        Model Depth 5
    Attributes:
    """

    


class GeneralContractorProperties(TypedDict):
    """A general contractor.

    References:
        https://schema.org/GeneralContractor
    Note:
        Model Depth 5
    Attributes:
    """

    

#GeneralContractorInheritedPropertiesTd = GeneralContractorInheritedProperties()
#GeneralContractorPropertiesTd = GeneralContractorProperties()


class AllProperties(GeneralContractorInheritedProperties , GeneralContractorProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GeneralContractorProperties, GeneralContractorInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "GeneralContractor"
    return model
    

GeneralContractor = create_schema_org_model()