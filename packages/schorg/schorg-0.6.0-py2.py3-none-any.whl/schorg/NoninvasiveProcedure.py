"""
A type of medical procedure that involves noninvasive techniques.

https://schema.org/NoninvasiveProcedure
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NoninvasiveProcedureInheritedProperties(TypedDict):
    """A type of medical procedure that involves noninvasive techniques.

    References:
        https://schema.org/NoninvasiveProcedure
    Note:
        Model Depth 6
    Attributes:
    """

    


class NoninvasiveProcedureProperties(TypedDict):
    """A type of medical procedure that involves noninvasive techniques.

    References:
        https://schema.org/NoninvasiveProcedure
    Note:
        Model Depth 6
    Attributes:
    """

    

#NoninvasiveProcedureInheritedPropertiesTd = NoninvasiveProcedureInheritedProperties()
#NoninvasiveProcedurePropertiesTd = NoninvasiveProcedureProperties()


class AllProperties(NoninvasiveProcedureInheritedProperties , NoninvasiveProcedureProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NoninvasiveProcedureProperties, NoninvasiveProcedureInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NoninvasiveProcedure"
    return model
    

NoninvasiveProcedure = create_schema_org_model()