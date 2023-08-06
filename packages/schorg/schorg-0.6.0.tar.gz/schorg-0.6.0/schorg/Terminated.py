"""
Terminated.

https://schema.org/Terminated
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TerminatedInheritedProperties(TypedDict):
    """Terminated.

    References:
        https://schema.org/Terminated
    Note:
        Model Depth 6
    Attributes:
    """

    


class TerminatedProperties(TypedDict):
    """Terminated.

    References:
        https://schema.org/Terminated
    Note:
        Model Depth 6
    Attributes:
    """

    

#TerminatedInheritedPropertiesTd = TerminatedInheritedProperties()
#TerminatedPropertiesTd = TerminatedProperties()


class AllProperties(TerminatedInheritedProperties , TerminatedProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TerminatedProperties, TerminatedInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Terminated"
    return model
    

Terminated = create_schema_org_model()