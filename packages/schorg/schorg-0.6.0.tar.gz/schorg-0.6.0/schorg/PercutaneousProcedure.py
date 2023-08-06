"""
A type of medical procedure that involves percutaneous techniques, where access to organs or tissue is achieved via needle-puncture of the skin. For example, catheter-based procedures like stent delivery.

https://schema.org/PercutaneousProcedure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PercutaneousProcedureInheritedProperties(TypedDict):
    """A type of medical procedure that involves percutaneous techniques, where access to organs or tissue is achieved via needle-puncture of the skin. For example, catheter-based procedures like stent delivery.

    References:
        https://schema.org/PercutaneousProcedure
    Note:
        Model Depth 6
    Attributes:
    """

    


class PercutaneousProcedureProperties(TypedDict):
    """A type of medical procedure that involves percutaneous techniques, where access to organs or tissue is achieved via needle-puncture of the skin. For example, catheter-based procedures like stent delivery.

    References:
        https://schema.org/PercutaneousProcedure
    Note:
        Model Depth 6
    Attributes:
    """

    

#PercutaneousProcedureInheritedPropertiesTd = PercutaneousProcedureInheritedProperties()
#PercutaneousProcedurePropertiesTd = PercutaneousProcedureProperties()


class AllProperties(PercutaneousProcedureInheritedProperties , PercutaneousProcedureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PercutaneousProcedureProperties, PercutaneousProcedureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PercutaneousProcedure"
    return model
    

PercutaneousProcedure = create_schema_org_model()