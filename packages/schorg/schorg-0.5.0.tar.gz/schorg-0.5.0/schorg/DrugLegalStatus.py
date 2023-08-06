"""
The legal availability status of a medical drug.

https://schema.org/DrugLegalStatus
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DrugLegalStatusInheritedProperties(TypedDict):
    """The legal availability status of a medical drug.

    References:
        https://schema.org/DrugLegalStatus
    Note:
        Model Depth 4
    Attributes:
    """

    


class DrugLegalStatusProperties(TypedDict):
    """The legal availability status of a medical drug.

    References:
        https://schema.org/DrugLegalStatus
    Note:
        Model Depth 4
    Attributes:
        applicableLocation: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The location in which the status applies.
    """

    applicableLocation: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#DrugLegalStatusInheritedPropertiesTd = DrugLegalStatusInheritedProperties()
#DrugLegalStatusPropertiesTd = DrugLegalStatusProperties()


class AllProperties(DrugLegalStatusInheritedProperties , DrugLegalStatusProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DrugLegalStatusProperties, DrugLegalStatusInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DrugLegalStatus"
    return model
    

DrugLegalStatus = create_schema_org_model()