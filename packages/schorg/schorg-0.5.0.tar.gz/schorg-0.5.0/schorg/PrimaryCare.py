"""
The medical care by a physician, or other health-care professional, who is the patient's first contact with the health-care system and who may recommend a specialist if necessary.

https://schema.org/PrimaryCare
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PrimaryCareInheritedProperties(TypedDict):
    """The medical care by a physician, or other health-care professional, who is the patient's first contact with the health-care system and who may recommend a specialist if necessary.

    References:
        https://schema.org/PrimaryCare
    Note:
        Model Depth 5
    Attributes:
    """

    


class PrimaryCareProperties(TypedDict):
    """The medical care by a physician, or other health-care professional, who is the patient's first contact with the health-care system and who may recommend a specialist if necessary.

    References:
        https://schema.org/PrimaryCare
    Note:
        Model Depth 5
    Attributes:
    """

    

#PrimaryCareInheritedPropertiesTd = PrimaryCareInheritedProperties()
#PrimaryCarePropertiesTd = PrimaryCareProperties()


class AllProperties(PrimaryCareInheritedProperties , PrimaryCareProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PrimaryCareProperties, PrimaryCareInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PrimaryCare"
    return model
    

PrimaryCare = create_schema_org_model()